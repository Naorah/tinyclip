/**
 * Compress a video file and stream the result
 * @param request - The request body { file: File, size: number, speed: number }
 * @returns The compressed video file
 */
export async function POST({ request }: { request: Request }) {
  const formData = await request.formData();

  try {
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
  } catch (error) {
    console.error('Error:', error);
    return new Response('Internal Server Error', { status: 500 });
  }

}

/**
 * Download a video file from the backend
 * @param request - The request body { token: string }
 * @returns The compressed video file
 */
export async function GET({ request }: { request: Request }) {
  const url = new URL(request.url);
  const token = url.searchParams.get('token');
  if (!token) {
    return new Response('Token is required', { status: 400 });
  }
  const response = await fetch(`http://127.0.0.1:5000/download?token=${token}`);
  return response;
}