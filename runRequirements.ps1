while ($response -notin @("y", "n")) {
    $response = Read-Host "Do you want to rescrape URLs(do this for newer data/no data)? This step takes a while (y/n)"

    if ($response -ne "y" -and $response -ne "n") {
        Write-Host "Please enter either 'y' or 'n'."
    }
}

if ($response -eq "y") {
    # Scrape URLs
    Start-Process -FilePath "python" -ArgumentList "./mainScraper.py" -Wait

    # Clean URLs
    Start-Process -FilePath "python" -ArgumentList "./util/cleanJSON.py" -Wait

    # Generate CSV
    Start-Process -FilePath "python" -ArgumentList "./carScraper.py" -Wait
}elseif ($response -eq "no") {
    # Skip this step
    Write-Host "Skipping URL scraping step..."

    # Generate CSV
    Start-Process -FilePath "python" -ArgumentList "./carScraper.py" -Wait

    Write-Host "Done, you should now use cars.csv inside the .ipynb file to generate this model"
}