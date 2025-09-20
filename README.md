# Address Dashboard

An example of using Dash to display recently created/updated addresses with a map and table. A practical use for such an application could be for a city department's internal function. One such case could be to highlight where addresses were recently created/updated could give insight into recent development in the city. Additionally, this example makes use of the Bootstrap grid system to align elements of the page, specifically to place space for key performance indicators above data table.

The contents of this project were based on the addresses available on the San Francisco open data portal. It is therefore not meant to be used as a template, but moreso as a project showcase. Creating a dashboard for a city's address data would require an exploring the available fields and how it could be displayed on a dashboard.


By default, the Dash app will showcase the last 7 days of created/updated addresses. Work to reliably retrieve address data asynchronously has not been achieved, but it would be a future goal. Currently the only way to view address data would be to export the data from the San Francisco open data portal as a CSV and place it in an accompanying `data` directory.
