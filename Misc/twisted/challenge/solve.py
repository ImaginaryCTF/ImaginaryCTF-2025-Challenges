import re
import ast
import numpy as np


def compute_umeyama_transformation(source_points, target_points, with_scale=True):
    source_center = source_points.mean(axis=0)
    target_center = target_points.mean(axis=0)

    source_centered = source_points - source_center
    target_centered = target_points - target_center

    num_points = source_points.shape[0]
    cross_covariance = (target_centered.T @ source_centered) / num_points

    U, singular_values, Vt = np.linalg.svd(cross_covariance)

    reflection_correction = np.eye(3)
    if np.linalg.det(U @ Vt) < 0:
        reflection_correction[2, 2] = -1.0

    rotation_matrix = U @ reflection_correction @ Vt

    source_variance = (source_centered**2).sum() / num_points
    scale_factor = (np.trace(np.diag(singular_values) @
                    reflection_correction) / source_variance) if with_scale else 1.0
    translation_vector = target_center - \
        scale_factor * (rotation_matrix @ source_center)

    return scale_factor, rotation_matrix, translation_vector


def apply_inverse_transformation(transformed_points, scale_factor, rotation_matrix, translation_vector):
    return ((transformed_points - translation_vector) / scale_factor) @ rotation_matrix


def clamp_to_byte_range(value):
    rounded_value = int(round(value))
    if rounded_value < 0:
        rounded_value += 256
    if rounded_value > 255:
        rounded_value -= 256
    return rounded_value


def iteratively_refine_transformation(target_points, initial_scale, initial_rotation, initial_translation, num_iterations=8):
    scale_factor = initial_scale
    rotation_matrix = initial_rotation
    translation_vector = initial_translation

    for _ in range(num_iterations):
        recovered_points = apply_inverse_transformation(
            target_points, scale_factor, rotation_matrix, translation_vector)
        clamped_points = np.array([[clamp_to_byte_range(
            value) for value in row] for row in recovered_points], dtype=float)
        scale_factor, rotation_matrix, translation_vector = compute_umeyama_transformation(
            clamped_points, target_points, with_scale=True)

    return scale_factor, rotation_matrix, translation_vector


def build_flag_string(recovered_matrix):
    flag_chars = ''.join(''.join(chr(clamp_to_byte_range(value))
                         for value in row) for row in recovered_matrix)
    return flag_chars.split('}', 1)[0] + '}' if '}' in flag_chars else flag_chars


def calculate_reconstruction_error(matrix):
    return float(np.sum(np.abs(matrix - np.round(matrix))))


def parse_input_data():
    user_input = input().strip()
    cleaned_input = re.sub(r'\barray\(', '(', user_input)
    parsed_array = ast.literal_eval(cleaned_input)
    data_matrix = np.array(parsed_array, dtype=float)

    if data_matrix.ndim == 1:
        data_matrix = np.array([data_matrix])

    return data_matrix


def generate_transformation_candidates(spatial_coordinates):
    candidate_list = []

    for sixth_character in range(32, 127):
        known_ascii_points = np.array(
            [[105, 99, 116], [102, 123, sixth_character], [125, 48, 48]], dtype=float)
        corresponding_transformed_points = np.stack(
            [spatial_coordinates[0], spatial_coordinates[1], spatial_coordinates[-1]], axis=0)

        initial_scale, initial_rotation, initial_translation = compute_umeyama_transformation(
            known_ascii_points, corresponding_transformed_points, with_scale=True)
        trial_reconstruction = apply_inverse_transformation(
            spatial_coordinates, initial_scale, initial_rotation, initial_translation)
        reconstruction_quality = calculate_reconstruction_error(
            trial_reconstruction)

        candidate_list.append((reconstruction_quality, sixth_character,
                              initial_scale, initial_rotation, initial_translation))

    candidate_list.sort(key=lambda x: x[0])
    return candidate_list


def find_best_flag_reconstruction(spatial_coordinates, sorted_candidates):
    best_flag_text = None
    best_reconstruction_score = None

    for _, sixth_character, initial_scale, initial_rotation, initial_translation in sorted_candidates[:20]:
        refined_scale, refined_rotation, refined_translation = iteratively_refine_transformation(
            spatial_coordinates, initial_scale, initial_rotation, initial_translation, num_iterations=12
        )

        final_reconstruction = apply_inverse_transformation(
            spatial_coordinates, refined_scale, refined_rotation, refined_translation)
        ascii_values = [clamp_to_byte_range(
            value) for value in final_reconstruction.flatten()]

        if any(not (32 <= value <= 126 or value == 48) for value in ascii_values):
            continue

        reconstructed_text = build_flag_string(final_reconstruction)
        current_score = calculate_reconstruction_error(final_reconstruction)

        if reconstructed_text.startswith('ictf{') and reconstructed_text.endswith('}'):
            if best_reconstruction_score is None or current_score < best_reconstruction_score:
                best_reconstruction_score = current_score
                best_flag_text = reconstructed_text

    return best_flag_text


data_matrix = parse_input_data()
spatial_coordinates = data_matrix[:, 1:4]

transformation_candidates = generate_transformation_candidates(
    spatial_coordinates)
best_flag = find_best_flag_reconstruction(
    spatial_coordinates, transformation_candidates)

if best_flag is None:
    _, fallback_char, fallback_scale, fallback_rotation, fallback_translation = transformation_candidates[
        0]
    refined_scale, refined_rotation, refined_translation = iteratively_refine_transformation(
        spatial_coordinates, fallback_scale, fallback_rotation, fallback_translation, num_iterations=12
    )
    best_flag = build_flag_string(apply_inverse_transformation(
        spatial_coordinates, refined_scale, refined_rotation, refined_translation))

print(best_flag)
