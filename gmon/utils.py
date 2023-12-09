import json

def generate_html(data, max_y=50):
    # Convert data to GB and process the data
    data_gb = [[mb / 1024 for mb in row] for row in data]
    gpu_data = list(zip(*data_gb))
    # HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GMON GPU Memory Usage Graph</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            .hidden {{ display: none; }}
            button {{                background-color: #4267B2; /* Facebook Blue */
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 5px;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            button:focus, button:hover {{
            background-color: #102757;
            outline:none;
            }}
            .container {{
            text-align:center;
            }}
            .graph {{
            padding:20px 50px 50px 50px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
        <h1>GMON GPU Memory Usage Over Time (in GB)</h1>

        {toggle_buttons}
        <div class="graph">{graphs}</div>

        </div>
        <script>
            var dataSets = {data_sets};
            var timeLabels = {time_labels};
            function showChart(gpuIndex) {{
                dataSets.forEach(function(_, index) {{
                    document.getElementById('chart-container' + index).style.display = index === gpuIndex ? 'block' : 'none';
                }});
            }}

            dataSets.forEach(function(data, index) {{
                var ctx = document.getElementById('chart' + index).getContext('2d');
                new Chart(ctx, {{
                    type: 'bar',
                    data: {{
                        labels: timeLabels,
                        datasets: [{{
                            label: 'GPU Memory ' + index,
                            data: data,
                            borderColor: 'rgb(75, 192, 192)',
                            backgroundColor: 'rgba(0, 123, 255, 0.6)',
                            tension: 0.1
                        }}]
                    }},
                    options: {{
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                max: {max_y},
                            }}
                        }}
                    }}
                }});
            }});

            // Initially show only the first chart
            showChart(0);
        </script>
    </body>
    <footer>Generated using <a target="_blank" href="https://github.com/AdamLouly/gmon">GMON</a></footer>
    </html>
    """

    # Create graph divs, toggle buttons, and JS data arrays
    graph_divs = []
    toggle_buttons = []
    data_sets = []
    time_labels = list(range(1, len(data) + 1))

    for i, gpu in enumerate(gpu_data):
        graph_divs.append(f'<div id="chart-container{i}" class="chart-container"><canvas id="chart{i}" width="300" height="150"></canvas></div>')
        toggle_buttons.append(f'<button onclick="showChart({i})">Show GPU {i}</button>')
        data_sets.append(list(gpu))

    # Finalize the HTML
    final_html = html_template.format(
        graphs='\n'.join(graph_divs),
        toggle_buttons='\n'.join(toggle_buttons),
        data_sets=json.dumps(data_sets),
        time_labels=json.dumps(time_labels),
        max_y=max_y
    )

    # Write to an HTML file
    with open('gmon_gpu_memory_usage.html', 'w') as file:
        file.write(final_html)
