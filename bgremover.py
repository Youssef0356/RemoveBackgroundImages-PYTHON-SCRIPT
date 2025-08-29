import os

# IMPORTANT: Set U2NET_HOME to the DIRECTORY that contains your model files
# (e.g. u2net.onnx). This must be set BEFORE importing rembg.
# Example for Windows:
# os.environ['U2NET_HOME'] = r"C:\\Users\\<Your_Username>\\Downloads"

os.environ['U2NET_HOME'] = r"C:\\Users\\PCNAME\\Downloads"

from rembg import remove, new_session


MODEL_NAME = "u2net"  # Change to "isnet-general-use" if you have that model instead
SESSION = new_session(MODEL_NAME)


def remove_background(input_path, output_path):
    """
    Removes the background from a single image using the rembg library.
    
    Args:
        input_path (str): The file path of the input image.
        output_path (str): The file path to save the output image without the background.
    """
    try:
        # Open the image file in binary read mode ('rb')
        with open(input_path, 'rb') as i:
            input_data = i.read()
        
        # Process the image to remove the background
        # The 'remove' function automatically finds the model in the folder
        # you specified with the REMBG_HOME environment variable.
        output_data = remove(input_data, session=SESSION)
        
        # Save the result in binary write mode ('wb')
        with open(output_path, 'wb') as o:
            o.write(output_data)
            
        print(f"Background successfully removed from {input_path} and saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: The file at {input_path} was not found. Please check the path.")
    except Exception as e:
        print(f"An unexpected error occurred while processing {input_path}: {e}")


if __name__ == "__main__":
    # --- Configuration Section ---
    # Set the name of the folder containing your input images.
    # Make sure this folder is in the same directory as your Python script.
    input_folder_name = "inputfoldername"
    # Suffix to append to the derived output folder name
    output_suffix = "BGREMOVED"  # e.g. becomes "<INPUT_NAME>BGREMOVED"
    # Whether to uppercase the derived output folder name (to match your first example)
    uppercase_output_name = True
    # --- End Configuration Section ---

    # Get the full path for the output folder
    base_output_name = input_folder_name.upper() if uppercase_output_name else input_folder_name
    derived_output_folder_name = f"{base_output_name}{output_suffix}"
    output_folder_path = os.path.join(os.getcwd(), derived_output_folder_name)
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        print(f"Created output folder: {output_folder_path}")

    # Get the full path for the input folder
    input_folder_path = os.path.join(os.getcwd(), input_folder_name)

    # Check if the input folder exists
    if not os.path.exists(input_folder_path):
        print(f"Error: Input folder '{input_folder_name}' not found. Please create it and add your images.")
    else:
        # Loop through all files in the input folder
        for filename in os.listdir(input_folder_path):
            # Check if the file is a common image type to avoid errors with other file types
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                # Construct the full file paths for input and output
                input_file_path = os.path.join(input_folder_path, filename)
                base_name, _ = os.path.splitext(filename)
                output_file_path = os.path.join(output_folder_path, f"{base_name}.png")
                
                # Call the function to remove the background
                remove_background(input_file_path, output_file_path)


