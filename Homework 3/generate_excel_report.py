"""
Excel Report Generator
Creates a comprehensive Excel report with benchmark results
"""

import json
from pathlib import Path
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

class ExcelReportGenerator:
    def __init__(self):
        """Initialize the Excel report generator."""
        self.workbook = openpyxl.Workbook()
        
        # Define styles
        self.header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        self.header_font = Font(bold=True, color="FFFFFF", size=12)
        self.title_font = Font(bold=True, size=14)
        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Color scales
        self.good_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        self.medium_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
        self.poor_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        self.improvement_fill = PatternFill(start_color="92D050", end_color="92D050", fill_type="solid")
    
    def create_summary_sheet(self, summary):
        """Create the summary sheet."""
        sheet = self.workbook.active
        sheet.title = "Summary"
        
        # Title
        sheet['A1'] = "GPT-4 Prompt Engineering Benchmark Results"
        sheet['A1'].font = Font(bold=True, size=16)
        sheet.merge_cells('A1:D1')
        
        # Subtitle
        sheet['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        sheet.merge_cells('A2:D2')
        
        sheet['A3'] = "(Using Prompt Engineering - Fine-tuning deprecated by OpenAI)"
        sheet['A3'].font = Font(italic=True, size=10)
        sheet.merge_cells('A3:D3')
        
        # Model Information
        row = 5
        sheet[f'A{row}'] = "Model Information"
        sheet[f'A{row}'].font = self.title_font
        sheet.merge_cells(f'A{row}:B{row}')
        
        row += 1
        sheet[f'A{row}'] = "Base Model:"
        sheet[f'B{row}'] = summary['base_model']
        sheet[f'A{row}'].font = Font(bold=True)
        
        row += 1
        sheet[f'A{row}'] = "Enhanced Model:"
        sheet[f'B{row}'] = summary['finetuned_model']
        sheet[f'A{row}'].font = Font(bold=True)
        
        row += 1
        sheet[f'A{row}'] = "Method:"
        sheet[f'B{row}'] = summary.get('method', 'Prompt Engineering')
        sheet[f'A{row}'].font = Font(bold=True)
        
        row += 1
        sheet[f'A{row}'] = "Total Test Cases:"
        sheet[f'B{row}'] = summary['total_test_cases']
        sheet[f'A{row}'].font = Font(bold=True)
        
        # Performance Metrics
        row += 2
        sheet[f'A{row}'] = "Performance Metrics"
        sheet[f'A{row}'].font = self.title_font
        sheet.merge_cells(f'A{row}:D{row}')
        
        row += 1
        # Headers
        headers = ['Metric', 'Base Model', 'Fine-tuned Model', 'Improvement']
        for col, header in enumerate(headers, 1):
            cell = sheet.cell(row=row, column=col)
            cell.value = header
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.border
        
        row += 1
        # Average Score
        sheet[f'A{row}'] = "Average Score (out of 10)"
        sheet[f'B{row}'] = summary['avg_base_score']
        sheet[f'C{row}'] = summary['avg_finetuned_score']
        sheet[f'D{row}'] = summary['avg_improvement']
        
        # Color code the improvement
        if summary['avg_improvement'] > 0:
            sheet[f'D{row}'].fill = self.improvement_fill
        
        for col in range(1, 5):
            sheet.cell(row=row, column=col).border = self.border
        
        row += 1
        sheet[f'A{row}'] = "Improvement Percentage"
        sheet[f'B{row}'] = "-"
        sheet[f'C{row}'] = "-"
        sheet[f'D{row}'] = f"{summary['improvement_percentage']}%"
        sheet[f'D{row}'].font = Font(bold=True)
        
        if summary['improvement_percentage'] > 0:
            sheet[f'D{row}'].fill = self.improvement_fill
        
        for col in range(1, 5):
            sheet.cell(row=row, column=col).border = self.border
        
        # Key Findings
        row += 2
        sheet[f'A{row}'] = "Key Findings"
        sheet[f'A{row}'].font = self.title_font
        sheet.merge_cells(f'A{row}:D{row}')
        
        row += 1
        findings = self.generate_findings(summary)
        for finding in findings:
            sheet[f'A{row}'] = f"• {finding}"
            sheet.merge_cells(f'A{row}:D{row}')
            row += 1
        
        # Adjust column widths
        sheet.column_dimensions['A'].width = 30
        sheet.column_dimensions['B'].width = 40
        sheet.column_dimensions['C'].width = 40
        sheet.column_dimensions['D'].width = 20
    
    def generate_findings(self, summary):
        """Generate key findings from the summary."""
        findings = []
        
            findings.append("Prompt engineering with few-shot examples is highly effective")
        elif improvement > 0:
            findings.append(f"Moderate improvement: +{improvement} points ({improvement_pct}% increase)")
            findings.append("Enhanced prompts provide measurable benefits")
        elif improvement < 0:
            findings.append(f"Unexpected decrease: {improvement} points ({improvement_pct}% decrease)")
        else:
            findings.append("No significant change in performance")
        
        if summary['avg_finetuned_score'] >= 8:
            findings.append("Enhanced model achieves excellent performance (8+/10)")
        elif summary['avg_finetuned_score'] >= 6:
            findings.append("Enhancficant change in performance")
        
        if summary['avg_finetuned_score'] >= 8:
            findings.append("Fine-tuned model achieves excellent performance (8+/10)")
        elif summary['avg_finetuned_score'] >= 6:
            findings.append("Enhanced model may need additional prompt optimization")
        
        if summary['total_test_cases'] < 10:
            findings.append(f"Limited test set ({summary['total_test_cases']} cases) - consider more comprehensive testing")
        
        findings.append("Note: Using prompt engineering due to OpenAI fine-tuning deprecation
        if summary['total_test_cases'] < 10:
            findings.append(f"Limited test set ({summary['total_test_cases']} cases) - consider more comprehensive testing")
        
        return findings
    
    def create_detailed_results_sheet(self, results):
        """Create detailed results sheet."""
        sheet = selfEnhanced Response', 'Enhancd Results")
        
        # Headers
        headers = ['#', 'Question', 'Expected Answer', 'Base Response', 'Base Score', 
                   'Fine-tuned Response', 'Fine-tuned Score', 'Improvement']
        
        for col, header in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col)
            cell.value = header
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center', vertical='top', wrap_text=True)
            cell.border = self.border
        
        # Data rows
        for row_idx, result in enumerate(results, 2):
            # Test case number
            cell = sheet.cell(row=row_idx, column=1)
            cell.value = result['test_case_id']
            cell.alignment = Alignment(horizontal='center', vertical='top')
            cell.border = self.border
            
            # Question
            cell = sheet.cell(row=row_idx, column=2)
            cell.value = result['question']
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            cell.border = self.border
            
            # Expected Answer
            cell = sheet.cell(row=row_idx, column=3)
            cell.value = result['expected_answer']
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            cell.border = self.border
            
            # Base Response
            cell = sheet.cell(row=row_idx, column=4)
            cell.value = result['base_response']
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            cell.border = self.border
            
            # Base Score
            cell = sheet.cell(row=row_idx, column=5)
            cell.value = result['base_score']
            cell.alignment = Alignment(horizontal='center', vertical='top')
            cell.border = self.border
            seEnhanced Response
            cell = sheet.cell(row=row_idx, column=6)
            cell.value = result['finetuned_response']
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            cell.border = self.border
            
            # Enhancr = self.border
            
            # Fine-tuned Score
            cell = sheet.cell(row=row_idx, column=7)
            cell.value = result['finetuned_score']
            cell.alignment = Alignment(horizontal='center', vertical='top')
            cell.border = self.border
            self.apply_score_color(cell, result['finetuned_score'])
            
            # Improvement
            cell = sheet.cell(row=row_idx, column=8)
            improvement = result['improvement']
            cell.value = f"+{improvement}" if improvement > 0 else str(improvement)
            cell.alignment = Alignment(horizontal='center', vertical='top')
            cell.border = self.border
            if improvement > 0:
                cell.fill = self.improvement_fill
                cell.font = Font(bold=True)
        
        # Adjust column widths
        sheet.column_dimensions['A'].width = 8
        sheet.column_dimensions['B'].width = 40
        sheet.column_dimensions['C'].width = 40
        sheet.column_dimensions['D'].width = 40
        sheet.column_dimensions['E'].width = 12
        sheet.column_dimensions['F'].width = 40
        sheet.column_dimensions['G'].width = 12
        sheet.column_dimensions['H'].width = 12
        
        # Set row height for better readability
        for row in range(2, len(results) + 2):
            sheet.row_dimensions[row].height = 60
    
    def apply_score_color(self, cell, score):
        """Apply color based on score."""
        if score >= 7:
            cell.fill = self.good_fill
        elif score >= 5:
            cell.fill = self.medium_fill
        else:
            cell.fill = self.poor_fill
    
    def create_comparison_sheet(self, results):
        """Create a comparison chart sheet."""
        sheet = self.workbook.create_sheet("Score Comparison")
        
        # Headers
        headers = ['Test Case', 'Question (Short)', 'Base Score', 'Enhanced Score', 'Improvement']
        for col, header in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col)
            cell.value = header
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.border
        
        # Data
        for row_idx, result in enumerate(results, 2):
            # Test case number
            sheet.cell(row=row_idx, column=1).value = result['test_case_id']
            sheet.cell(row=row_idx, column=1).alignment = Alignment(horizontal='center')
            sheet.cell(row=row_idx, column=1).border = self.border
            
            # Question (truncated)
            question_short = result['question'][:50] + "..." if len(result['question']) > 50 else result['question']
            sheet.cell(row=row_idx, column=2).value = question_short
            sheet.cell(row=row_idx, column=2).border = self.border
            
            # Base Score
            cell = sheet.cell(row=row_idx, column=3)
            cell.value = result['base_score']
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.border
            
            # Fine-tuned Score
            cell = sheet.cell(row=row_idx, column=4)
            cell.value = result['finetuned_score']
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.border
            
            # Improvement
            cell = sheet.cell(row=row_idx, column=5)
            improvement = result['improvement']
            cell.value = improvement
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.border
            if improvement > 0:
                cell.fill = self.improvement_fill
        
        # Adjust column widths
        sheet.column_dimensions['A'].width = 12
        sheet.column_dimensions['B'].width = 50
        sheet.column_dimensions['C'].width = 15
        sheet.column_dimensions['D'].width = 15
        sheet.column_dimensions['E'].width = 15
    
    def generate_report(self, results, summary, output_file="Homework3_Benchmark_Results.xlsx"):
        """Generate the complete Excel report."""
        print("📊 Generating Excel report...")
        
        # Create sheets
        self.create_summary_sheet(summary)
        self.create_detailed_results_sheet(results)
        self.create_comparison_sheet(results)
        
        # Save workbook
        output_path = Path(__file__).parent / output_file
        self.workbook.save(output_path)
        
        print(f"✅ Excel report saved to: {output_path}")
        return output_path


def main():
    """Main execution function."""
    # Load benchmark results
    results_file = Path(__file__).parent / "benchmark_results.json"
    
    if not results_file.exists():
        print("❌ Benchmark results not found. Please run benchmark_models.py first.")
        return
    
    print("📥 Loading benchmark results...")
    with open(results_file, encoding="utf-8") as f:
        data = json.load(f)
    
    results = data['results']
    summary = data['summary']
    
    print(f"✅ Loaded {len(results)} test results")
    
    # Generate Excel report
    generator = ExcelReportGenerator()
    output_path = generator.generate_report(results, summary)
    
    print("\n🎉 Excel report generation complete!")
    print(f"📄 Report: {output_path}")


if __name__ == "__main__":
    main()
