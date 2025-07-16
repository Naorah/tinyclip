import { error } from "@sveltejs/kit";


// ##### ALLOWED TYPES #####
const allowed_types = [
  'video/webm', 
  'video/mkv', 
  'video/flv', 
  'video/vob', 
  'video/ogv', 
  'video/ogg', 
  'video/rrc', 
  'video/gifv', 
  'video/mng', 
  'video/mov', 
  'video/avi', 
  'video/qt', 
  'video/wmv', 
  'video/yuv', 
  'video/rm', 
  'video/asf', 
  'video/amv', 
  'video/mp4', 
  'video/m4p', 
  'video/m4v', 
  'video/mpg', 
  'video/mp2', 
  'video/mpeg', 
  'video/mpe', 
  'video/mpv', 
  'video/m4v', 
  'video/svi', 
  'video/3gp', 
  'video/3g2', 
  'video/mxf', 
  'video/roq', 
  'video/nsv', 
  'video/flv', 
  'video/f4v', 
  'video/f4p', 
  'video/f4a', 
  'video/f4b', 
  'video/mod'
];

/**
 * Validate the video data
 * @param file - The video file to validate
 * @param size - The target size of the compressed video in bytes
 * @param speed - The speed factor for the compression
 */
async function validateVideoData(file: File, size: number, speed: number) {
  if (!file) {
    return{code: 400, message: 'File is required'};
  }

  if (!allowed_types.includes(file.type)) {
    return{code: 400, message: 'File must be an MP4, MKV, WEBM, FLV, VOB, OGV, OGG, RRC, GIFV, MNG, MOV, AVI, QT, WMV, YUV, RM, ASF, AMV, MP4, M4P, M4V, MPG, MP2, MPEG, MPE, MPV, M4V, SVI, 3GP, 3G2, MXF, ROQ, NSV, FLV, F4V, F4P, F4A, F4B, MOD'};
  }
  
  const input_max_size_allowed = (1024 * 1024 * 1024) * 5; // 5GB

  const output_max_size_allowed = 1024 * 3 // 3GB
  
  if (file.size > input_max_size_allowed) {
    return{code: 400, message: 'File must be less than 5GB'};
  }
  
  if (size <= 0 || size > output_max_size_allowed) {
    return{code: 400, message: 'Size must be between 0 and 1GB'};
  }
  
  if (!Number.isInteger(speed) || speed <= 0) {
    return{code: 400, message: 'Speed must be a positive integer'};
  }

  return {code: 200, message: 'Video data is valid'};
}

/**
 * Compress a video file
 * @param file - The video file to compress
 * @param size - The target size of the compressed video in bytes
 * @param speed - The speed factor for the compression
 * @returns The compressed video file
 */
export async function compressVideoStream(file: File, size: number, speed: number) {
  const validation_response = await validateVideoData(file, size, speed);
  if (validation_response.code !== 200) {
    return{code: validation_response.code, message: validation_response.message};
  }

  const formData = new FormData();
  formData.append('file', file);
  formData.append('size', size.toString());
  formData.append('speed', speed.toString());

  const response = await fetch('/api/video/stream', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    return new Response('Failed to compress video', { status: 500 });
  }

  return response.body;
};

export async function downloadVideo(token: string) {
  const response = await fetch(`/api/video/stream?token=${token}`);
  if (!response.ok) {
    return{code: 500, message: 'Failed to download video'};
  }

  return response.blob();
};