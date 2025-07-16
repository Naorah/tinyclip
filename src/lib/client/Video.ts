import { error } from "@sveltejs/kit";

/**
 * Validate the video data
 * @param file - The video file to validate
 * @param size - The target size of the compressed video in bytes
 * @param speed - The speed factor for the compression
 */
async function validateVideoData(file: File, size: number, speed: number) {
  if (!file) {
    error(400, 'File is required');
  }

  if (file.type !== 'video/mp4') {
    error(400, 'File must be an MP4 video');
  }
  
  const oneGB = 1024 * 1024 * 1024; // 1GB
  
  if (file.size > oneGB) {
    error(400, 'File must be less than 1GB');
  }
  
  if (size <= 0 || size > oneGB) {
    error(400, 'Size must be between 0 and 1GB');
  }
  
  if (!Number.isInteger(speed) || speed <= 0) {
    error(400, 'Speed must be a positive integer');
  }
}

/**
 * Compress a video file
 * @param file - The video file to compress
 * @param size - The target size of the compressed video in bytes
 * @param speed - The speed factor for the compression
 * @returns The compressed video file
 */
export async function compressVideo(file: File, size: number, speed: number) {
  validateVideoData(file, size, speed);

  const formData = new FormData();
  formData.append('file', file);
  formData.append('size', size.toString());
  formData.append('speed', speed.toString());

  const response = await fetch('/api/video', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    error(500, 'Failed to compress video');
  }

  return response.blob();
};

/**
 * Compress a video file
 * @param file - The video file to compress
 * @param size - The target size of the compressed video in bytes
 * @param speed - The speed factor for the compression
 * @returns The compressed video file
 */
export async function compressVideoStream(file: File, size: number, speed: number) {
  validateVideoData(file, size, speed);

  const formData = new FormData();
  formData.append('file', file);
  formData.append('size', size.toString());
  formData.append('speed', speed.toString());

  const response = await fetch('/api/video/stream', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    error(500, 'Failed to compress video');
  }

  return response.body;
};

export async function downloadVideo(path: string) {
  const response = await fetch(`/api/video/stream?path=${path}`);
  return response.blob();
};