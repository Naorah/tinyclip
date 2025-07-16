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

  const response = await fetch('http://127.0.0.1:5000/compress/stream', {
    method: 'POST',
    body: formData
  });
  return response.blob();
}

/**
 * Compress a video file and stream the result
 * @param request - The request body { file: File, size: number, speed: number }
 * @returns The compressed video file
 */
export async function POST({ request }: { request: Request }) {
  const formData = await request.formData();

  const backendResponse = await fetch('http://127.0.0.1:5000/compress/stream', {
    method: 'POST',
    body: formData,
  });

  return new Response(backendResponse.body, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    }
  });
}

/**
 * Download a video file from the backend
 * @param request - The request body { path: string }
 * @returns The compressed video file
 */
export async function GET({ request }: { request: Request }) {
  const url = new URL(request.url);
  const path = url.searchParams.get('path');
  if (!path) {
    return new Response('Path is required', { status: 400 });
  }
  const response = await fetch(`http://127.0.0.1:5000/download?path=${path}`);
  return response;
}