import { error } from '@sveltejs/kit';

/**
 * Calls the backend to compress a video file
 * @param file - The video file to compress
 * @param size - The target size of the compressed video in MB
 * @param speed - The speed factor for the compression
 * @returns The compressed video file
 */
async function callBackend(file: File, size: number, speed: number) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('size', size.toString());
  formData.append('speed', speed.toString());

  const response = await fetch('http://127.0.0.1:5000/compress', {
    method: 'POST',
    body: formData
  });
  return response.blob();
}

/**
 * Compresses a video file
 * @param request - The request body { file: File, size: number, speed: number }
 * @returns The compressed video file
 */
export async function POST({ request }: { request: Request }) {
  const formData = await request.formData();
  const file = formData.get('file') as File;

  const final_size = Number(formData.get('size')?.toString() ?? '10');
  const speed = parseFloat(formData.get('speed')?.toString() ?? '1');

  if (!file) throw error(400, 'Missing file');

  const compressedBuffer = await callBackend(file, final_size, speed);

  return new Response(compressedBuffer, {
    headers: {
      'Content-Type': 'video/mp4',
      'Content-Disposition': `attachment; filename=compressed-${file.name}`
    }
  });
}