"""
OpenAI GPT-4 Fine-tuning Script
This script handles the entire fine-tuning process for OpenAI models.
"""

import os
import json
import time
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OpenAIFineTuner:
    def __init__(self, api_key=None):
        """Initialize the OpenAI client."""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.training_file_id = None
        self.validation_file_id = None
        self.fine_tuned_model = None
        self.job_id = None
        
    def upload_file(self, file_path, purpose="fine-tune"):
        """Upload a file to OpenAI."""
        print(f"📤 Uploading {file_path}...")
        try:
            with open(file_path, "rb") as f:
                response = self.client.files.create(
                    file=f,
                    purpose=purpose
                )
            print(f"✅ File uploaded successfully! ID: {response.id}")
            return response.id
        except Exception as e:
            print(f"❌ Error uploading file: {e}")
            raise
    
    def create_fine_tuning_job(self, training_file_id, validation_file_id=None, 
                               model="gpt-4o-mini-2024-07-18", suffix=None):
        """Create a fine-tuning job."""
        print(f"🚀 Creating fine-tuning job for model: {model}")
        try:
            params = {
                "training_file": training_file_id,
                "model": model,
            }
            
            if validation_file_id:
                params["validation_file"] = validation_file_id
            
            if suffix:
                params["suffix"] = suffix
            
            job = self.client.fine_tuning.jobs.create(**params)
            
            print(f"✅ Fine-tuning job created! Job ID: {job.id}")
            print(f"📊 Status: {job.status}")
            return job
        except Exception as e:
            print(f"❌ Error creating fine-tuning job: {e}")
            raise
    
    def wait_for_completion(self, job_id, check_interval=60):
        """Wait for the fine-tuning job to complete."""
        print(f"⏳ Waiting for fine-tuning job {job_id} to complete...")
        print(f"   (Checking every {check_interval} seconds)")
        
        while True:
            try:
                job = self.client.fine_tuning.jobs.retrieve(job_id)
                status = job.status
                
                print(f"📊 Current status: {status}")
                
                if status == "succeeded":
                    print(f"✅ Fine-tuning completed successfully!")
                    print(f"🎯 Fine-tuned model: {job.fine_tuned_model}")
                    return job
                elif status == "failed":
                    print(f"❌ Fine-tuning failed!")
                    if hasattr(job, 'error'):
                        print(f"Error: {job.error}")
                    raise Exception("Fine-tuning job failed")
                elif status == "cancelled":
                    print(f"⚠️ Fine-tuning job was cancelled")
                    raise Exception("Fine-tuning job was cancelled")
                
                time.sleep(check_interval)
            except KeyboardInterrupt:
                print("\n⚠️ Monitoring interrupted by user")
                raise
            except Exception as e:
                if "failed" in str(e).lower() or "cancelled" in str(e).lower():
                    raise
                print(f"⚠️ Error checking status: {e}")
                time.sleep(check_interval)
    
    def get_job_events(self, job_id):
        """Get events for a fine-tuning job."""
        try:
            events = self.client.fine_tuning.jobs.list_events(job_id)
            return list(events)
        except Exception as e:
            print(f"⚠️ Error getting job events: {e}")
            return []
    
    def list_fine_tuned_models(self):
        """List all fine-tuned models."""
        try:
            models = self.client.models.list()
            fine_tuned = [m for m in models if m.id.startswith("ft:")]
            return fine_tuned
        except Exception as e:
            print(f"⚠️ Error listing models: {e}")
            return []
    
    def run_full_pipeline(self, train_file_path, validation_file_path=None, 
                         model="gpt-4o-mini-2024-07-18", suffix="hotel-booking"):
        """Run the complete fine-tuning pipeline."""
        print("=" * 60)
        print("🎯 Starting OpenAI Fine-tuning Pipeline")
        print("=" * 60)
        
        # Step 1: Upload training file
        print("\n📝 Step 1: Uploading training data")
        self.training_file_id = self.upload_file(train_file_path)
        
        # Step 2: Upload validation file (if provided)
        if validation_file_path and os.path.exists(validation_file_path):
            print("\n📝 Step 2: Uploading validation data")
            self.validation_file_id = self.upload_file(validation_file_path)
        else:
            print("\n⏭️ Step 2: Skipping validation file upload")
            self.validation_file_id = None
        
        # Step 3: Create fine-tuning job
        print("\n🚀 Step 3: Creating fine-tuning job")
        job = self.create_fine_tuning_job(
            self.training_file_id,
            self.validation_file_id,
            model,
            suffix
        )
        self.job_id = job.id
        
        # Step 4: Wait for completion
        print("\n⏳ Step 4: Waiting for fine-tuning to complete")
        completed_job = self.wait_for_completion(self.job_id)
        self.fine_tuned_model = completed_job.fine_tuned_model
        
        # Step 5: Summary
        print("\n" + "=" * 60)
        print("✅ Fine-tuning Pipeline Complete!")
        print("=" * 60)
        print(f"Fine-tuned Model ID: {self.fine_tuned_model}")
        print(f"Training File ID: {self.training_file_id}")
        if self.validation_file_id:
            print(f"Validation File ID: {self.validation_file_id}")
        print(f"Job ID: {self.job_id}")
        
        # Save results
        self.save_results()
        
        return {
            "fine_tuned_model": self.fine_tuned_model,
            "job_id": self.job_id,
            "training_file_id": self.training_file_id,
            "validation_file_id": self.validation_file_id
        }
    
    def save_results(self, output_file="finetune_results.json"):
        """Save fine-tuning results to a JSON file."""
        results = {
            "fine_tuned_model": self.fine_tuned_model,
            "job_id": self.job_id,
            "training_file_id": self.training_file_id,
            "validation_file_id": self.validation_file_id,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        output_path = Path(__file__).parent / output_file
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_path}")
        return output_path


def main():
    """Main execution function."""
    # Define paths
    base_dir = Path(__file__).parent / "hotel_booking_finetuning" / "openai_format"
    train_file = base_dir / "train.jsonl"
    validation_file = base_dir / "validation.jsonl"
    
    # Check if files exist
    if not train_file.exists():
        print(f"❌ Training file not found: {train_file}")
        return
    
    print(f"✅ Training file found: {train_file}")
    if validation_file.exists():
        print(f"✅ Validation file found: {validation_file}")
    else:
        print(f"⚠️ Validation file not found: {validation_file}")
        validation_file = None
    
    # Initialize fine-tuner
    finetuner = OpenAIFineTuner()
    
    # Run the pipeline
    # Note: Using gpt-4o-mini as gpt-4 fine-tuning may not be available or very expensive
    results = finetuner.run_full_pipeline(
        train_file_path=str(train_file),
        validation_file_path=str(validation_file) if validation_file else None,
        model="gpt-4o-mini-2024-07-18",  # More affordable alternative
        suffix="hotel-booking"
    )
    
    print("\n🎉 All done! You can now use the fine-tuned model for inference.")
    print(f"Model ID: {results['fine_tuned_model']}")


if __name__ == "__main__":
    main()
