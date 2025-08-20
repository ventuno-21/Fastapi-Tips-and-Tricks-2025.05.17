import './App.css'

import { Api } from './client'
import { useQuery } from '@tanstack/react-query'
import { AxiosError } from 'axios'


const api = new Api({
  baseURL: 'http://localhost:8000',
})

function App() {

  const id = "237f2f79-8a94-4b1f-8fcb-92a4cec89280"

  const { isLoading, isError, error, data } = useQuery({
    queryKey: [id],
    queryFn: async () => {
      const response = await api.shipmentv3.getShipment({ id })
      return response.data
    },
    retry: false,
  })

  if (isError) {
    const apiError = error as AxiosError

    return <p>Status Code: {apiError.status}</p>
  }

  if (isLoading || !data) {
    return <p>Loading...</p>
  }

  return (
    <>
      <div className='card'>
        <p>Id: #{data.id}</p>
        <p>Content: {data.content}</p>
        <p>Status: {data.timeline[data.timeline.length - 1].status}</p>
      </div>
    </>
  )
}

export default App
