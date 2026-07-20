import io
from PIL import Image


def visualize(graph, output_file_name):
    try:
        png = graph.get_graph().draw_mermaid_png()
        pil_image = Image.open(io.BytesIO(png))
        pil_image.save(output_file_name, "PNG")
    except Exception:
        # Optional — requires extra dependencies
        pass
