import type { HttpError } from '@/types/Error'
import { mockFindDogs } from './findDogs.mock'

function statusCodeToHttpError(statusCode: number): HttpError {
  if (statusCode === 400) return 'BadRequest'
  if (statusCode === 404) return 'NotFound'
  return 'InternalServerError'
}

export async function findDogs(query: string, error?: HttpError) {
  if (import.meta.env.VITE_MOCK_MODE === 'true') {
    return mockFindDogs(error)
  }

  const response = await fetch(`${import.meta.env.VITE_BACKEND_API_URL}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  })

  const json = await response.json()

  if (!response.ok) {
    throw statusCodeToHttpError(response.status)
  }

  return json.results
}
