const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

export async function submitReview(code, language) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/review`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code, language }),
    });

    if (!response.ok) {
      // If it's a 4xx or 5xx, try to extract the JSON error message
      const errorData = await response.json().catch(() => null);
      if (errorData && errorData.detail) {
        throw new Error(errorData.detail);
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}
