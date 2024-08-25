import math
import numpy as np
import json
import struct
import logging
import os
from scipy.spatial.transform import Rotation

# Set up more detailed logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('texture_transform.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Add a stream handler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def get_accessor_data(gltf_data, buffer_data, accessor_index):
    logger.debug(f"Getting accessor data for index {accessor_index}")
    accessor = gltf_data['accessors'][accessor_index]
    buffer_view = gltf_data['bufferViews'][accessor['bufferView']]
    start = buffer_view['byteOffset'] + accessor.get('byteOffset', 0)
    count = accessor['count']
    component_type = accessor['componentType']
    type = accessor['type']

    logger.debug(f"Accessor details: start={start}, count={count}, component_type={component_type}, type={type}")

    if component_type == 5126:  # FLOAT
        if type == 'VEC2':
            data = np.frombuffer(buffer_data[start:start + count * 8], dtype=np.float32).reshape(-1, 2)
        elif type == 'VEC3':
            data = np.frombuffer(buffer_data[start:start + count * 12], dtype=np.float32).reshape(-1, 3)
    elif component_type == 5123:  # UNSIGNED_SHORT
        data = np.frombuffer(buffer_data[start:start + count * 2], dtype=np.uint16)
    elif component_type == 5125:  # UNSIGNED_INT
        data = np.frombuffer(buffer_data[start:start + count * 4], dtype=np.uint32)
    else:
        raise ValueError(f"Unsupported component type: {component_type}")

    logger.debug(f"Retrieved data shape: {data.shape}")
    return data

def set_accessor_data(gltf_data, buffer_data, accessor_index, data):
    logger.debug(f"Setting accessor data for index {accessor_index}")
    accessor = gltf_data['accessors'][accessor_index]
    buffer_view = gltf_data['bufferViews'][accessor['bufferView']]
    start = buffer_view['byteOffset'] + accessor.get('byteOffset', 0)
    end = start + data.nbytes
    buffer_data[start:end] = data.tobytes()
    logger.debug(f"Updated buffer data from index {start} to {end}")

    # Update accessor min and max
    if accessor['componentType'] in [5126, 5123, 5125]:  # FLOAT, UNSIGNED_SHORT, UNSIGNED_INT
        accessor['min'] = data.min(axis=0).tolist()
        accessor['max'] = data.max(axis=0).tolist()

def scale_positions(positions, scale_factor):
    logger.debug(f"Scaling positions by factor {scale_factor}")
    scaled = positions * scale_factor
    logger.debug(f"Original positions range: {positions.min()} to {positions.max()}")
    logger.debug(f"Scaled positions range: {scaled.min()} to {scaled.max()}")
    return scaled

def apply_texture_transform(uv, transform):
    logger.debug(f"Applying texture transform: {transform}")
    offset = transform.get('offset', [0, 0])
    rotation = transform.get('rotation', 0)
    scale = transform.get('scale', [1, 1])
    
    logger.debug(f"Original UV: {uv}")
    
    # Apply scale
    uv[0] *= scale[0]
    uv[1] *= scale[1]
    logger.debug(f"After scale: {uv}")
    
    # Apply rotation
    if rotation != 0:
        cos_r = math.cos(rotation)
        sin_r = math.sin(rotation)
        x, y = uv
        uv[0] = x * cos_r - y * sin_r
        uv[1] = x * sin_r + y * cos_r
        logger.debug(f"After rotation: {uv}")
    
    # Apply offset
    uv[0] += offset[0]
    uv[1] += 1 - offset[1]  # Flip Y-axis offset
    logger.debug(f"After offset: {uv}")
    
    return uv

def process_gltf(gltf_data, buffer_data):
    logger.info("Starting GLTF processing")
    scale_factor = 100  # Increased to 100 to make geometry extremely large
    logger.info(f"Using scale factor: {scale_factor}")
    
    logger.info(f"Number of meshes: {len(gltf_data['meshes'])}")
    
    for mesh_index, mesh in enumerate(gltf_data['meshes']):
        logger.info(f"Processing mesh {mesh_index}")
        for primitive_index, primitive in enumerate(mesh['primitives']):
            logger.info(f"Processing primitive {primitive_index} of mesh {mesh_index}")
            logger.info(f"Primitive attributes: {primitive['attributes']}")
            
            # Scale positions
            if 'POSITION' in primitive['attributes']:
                position_accessor_index = primitive['attributes']['POSITION']
                positions = get_accessor_data(gltf_data, buffer_data, position_accessor_index)
                
                logger.info(f"Original positions shape: {positions.shape}")
                logger.info(f"Original positions min: {positions.min()}, max: {positions.max()}")
                
                positions *= scale_factor
                
                logger.info(f"Scaled positions shape: {positions.shape}")
                logger.info(f"Scaled positions min: {positions.min()}, max: {positions.max()}")
                
                set_accessor_data(gltf_data, buffer_data, position_accessor_index, positions)
                logger.info(f"Scaled positions for primitive {primitive_index}")
                logger.info(f"Updated accessor: min={gltf_data['accessors'][position_accessor_index]['min']}, max={gltf_data['accessors'][position_accessor_index]['max']}")
            
            # Process texture transform if present
            if 'material' in primitive:
                material = gltf_data['materials'][primitive['material']]
                if 'extensions' in material and 'KHR_texture_transform' in material['extensions']:
                    transform = material['extensions']['KHR_texture_transform']
                    logger.info(f"Found KHR_texture_transform: {transform}")
                    
                    # Get TEXCOORD_0 accessor
                    texcoord_index = primitive['attributes']['TEXCOORD_0']
                    uv_data = get_accessor_data(gltf_data, buffer_data, texcoord_index)
                    
                    logger.info(f"Original UV data shape: {uv_data.shape}")
                    logger.info(f"Original UV data min: {uv_data.min()}, max: {uv_data.max()}")
                    
                    # Apply transform to each UV coordinate
                    new_uv_data = np.array([apply_texture_transform(uv, transform) for uv in uv_data])
                    
                    logger.info(f"Transformed UV data shape: {new_uv_data.shape}")
                    logger.info(f"Transformed UV data min: {new_uv_data.min()}, max: {new_uv_data.max()}")
                    
                    # Update buffer with new UV data
                    set_accessor_data(gltf_data, buffer_data, texcoord_index, new_uv_data)
                    logger.info(f"Updated UV data for primitive {primitive_index}")
                    
                    # Remove the extension
                    del material['extensions']['KHR_texture_transform']
                    if not material['extensions']:
                        del material['extensions']
                    logger.info(f"Removed KHR_texture_transform extension from material")

    # Remove KHR_texture_transform from extensionsUsed and extensionsRequired
    for ext_list in ['extensionsUsed', 'extensionsRequired']:
        if ext_list in gltf_data:
            original_extensions = gltf_data[ext_list]
            gltf_data[ext_list] = [ext for ext in gltf_data[ext_list] if ext != 'KHR_texture_transform']
            logger.info(f"Removed KHR_texture_transform from {ext_list}. Original: {original_extensions}, Updated: {gltf_data[ext_list]}")

    logger.info("GLTF processing completed")
    return gltf_data, buffer_data

def bake_texture_transform(input_file, output_file):
    try:
        logger.info(f"Starting texture transform baking process for {input_file}")
        logger.info(f"Output file: {output_file}")
        # Read the GLB file
        with open(input_file, 'rb') as f:
            data = f.read()

        logger.info(f"File size: {len(data)} bytes")

        # Extract the JSON chunk
        magic = data[:4]
        if magic != b'glTF':
            raise ValueError("Invalid GLB file: magic number not found")

        version, length = struct.unpack('<II', data[4:12])
        if version != 2:
            raise ValueError(f"Unsupported GLB version: {version}")

        chunk_length, chunk_type = struct.unpack('<II', data[12:20])
        if chunk_type != 0x4E4F534A:  # JSON chunk type
            raise ValueError("First chunk is not JSON")

        json_data = data[20:20+chunk_length]
        
        logger.info(f"JSON chunk size: {len(json_data)} bytes")

        # Parse the JSON data
        gltf_data = json.loads(json_data)

        # Extract the binary buffer data
        buffer_start = 20 + chunk_length
        chunk_length, chunk_type = struct.unpack('<II', data[buffer_start:buffer_start+8])
        if chunk_type != 0x004E4942:  # BIN chunk type
            raise ValueError("Second chunk is not BIN")

        buffer_data = data[buffer_start+8:buffer_start+8+chunk_length]

        # Process the GLTF data
        processed_gltf_data, processed_buffer_data = process_gltf(gltf_data, buffer_data)
        logger.info("GLTF data processing completed")

        # Convert the modified JSON back to bytes
        modified_json = json.dumps(processed_gltf_data).encode('utf-8')

        logger.info(f"Modified JSON chunk size: {len(modified_json)} bytes")

        # Pad the JSON to maintain 4-byte alignment
        padding = (4 - (len(modified_json) % 4)) % 4
        modified_json += b' ' * padding

        # Construct the GLB file
        glb_header = struct.pack('<4sII', b'glTF', 2, 12 + len(modified_json) + 8 + len(processed_buffer_data))
        json_header = struct.pack('<II', len(modified_json), 0x4E4F534A)  # 'JSON' in little endian
        bin_header = struct.pack('<II', len(processed_buffer_data), 0x004E4942)  # 'BIN\0' in little endian

        # Write the new GLB file
        with open(output_file, 'wb') as f:
            f.write(glb_header)
            f.write(json_header)
            f.write(modified_json)
            f.write(bin_header)
            f.write(processed_buffer_data)

        logger.info(f"Saved processed file to {output_file}")
        logger.info(f"Final file size: {os.path.getsize(output_file)} bytes")
    except Exception as e:
        logger.error(f"Error during texture transform baking: {str(e)}")
        logger.exception("Stack trace:")
        raise

if __name__ == "__main__":
    input_file = "scene2.glb"
    output_file = "scene2_baked.glb"
    bake_texture_transform(input_file, output_file)
