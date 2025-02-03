# Exemple : envoi de 120 requêtes avec des valeurs légèrement variées
for ($i = 1; $i -le 120; $i++) {
    $body = @{
        Date        = 20250205 + $i
        Location    = (Get-Random -Minimum 1 -Maximum 10)
        MinTemp     = [math]::Round((Get-Random -Minimum 5.0 -Maximum 15.0),1)
        MaxTemp     = [math]::Round((Get-Random -Minimum 20.0 -Maximum 30.0),1)
        Rainfall    = [math]::Round((Get-Random -Minimum 0.0 -Maximum 2.0),1)
        Evaporation = [math]::Round((Get-Random -Minimum 3.0 -Maximum 6.0),1)
        Sunshine    = [math]::Round((Get-Random -Minimum 5.0 -Maximum 12.0),1)
        WindGustDir = (Get-Random -Minimum 0 -Maximum 360)
        WindGustSpeed = [math]::Round((Get-Random -Minimum 20.0 -Maximum 50.0),1)
        WindDir9am  = (Get-Random -Minimum 0 -Maximum 360)
        WindDir3pm  = (Get-Random -Minimum 0 -Maximum 360)
        WindSpeed9am = [math]::Round((Get-Random -Minimum 5.0 -Maximum 25.0),1)
        WindSpeed3pm = [math]::Round((Get-Random -Minimum 10.0 -Maximum 30.0),1)
        Humidity9am = [math]::Round((Get-Random -Minimum 40.0 -Maximum 90.0),1)
        Humidity3pm = [math]::Round((Get-Random -Minimum 30.0 -Maximum 70.0),1)
        Pressure9am = [math]::Round((Get-Random -Minimum 1000.0 -Maximum 1025.0),1)
        Pressure3pm = [math]::Round((Get-Random -Minimum 1000.0 -Maximum 1020.0),1)
        Cloud9am    = [math]::Round((Get-Random -Minimum 0.0 -Maximum 10.0),1)
        Cloud3pm    = [math]::Round((Get-Random -Minimum 0.0 -Maximum 10.0),1)
        Temp9am     = [math]::Round((Get-Random -Minimum 5.0 -Maximum 20.0),1)
        Temp3pm     = [math]::Round((Get-Random -Minimum 15.0 -Maximum 30.0),1)
        RainToday   = (Get-Random -Minimum 0 -Maximum 2)  # 0 ou 1
    } | ConvertTo-Json

    Invoke-RestMethod -Method Post -Uri http://localhost:8101/predict `
        -Headers @{ "Content-Type" = "application/json" } `
        -Body $body
    Start-Sleep -Seconds 1
}