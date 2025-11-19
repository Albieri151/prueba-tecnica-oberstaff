Write-Host "Cargando datos de prueba en Supabase..."

Invoke-RestMethod `
  -Uri "https://plwbyiubbjhaogbvtvqe.supabase.co/rest/v1/subscriptions" `
  -Method Post `
  -Headers @{
    "apikey" = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBsd2J5aXViYmpoYW9nYnZ0dnFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0MDIyNjgsImV4cCI6MjA3ODk3ODI2OH0.b5NAgOIYU7P0ZoOXBmwoZJyedoIzsI7k6SxnV5m3QbU"
    "Authorization" = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBsd2J5aXViYmpoYW9nYnZ0dnFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0MDIyNjgsImV4cCI6MjA3ODk3ODI2OH0.b5NAgOIYU7P0ZoOXBmwoZJyedoIzsI7k6SxnV5m3QbU"
    "Content-Type" = "application/json"
  } `
  -InFile "subscriptions.json"

Write-Host "Carga finalizada."
