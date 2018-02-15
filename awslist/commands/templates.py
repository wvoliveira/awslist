TEMPLATES = {'default': ["""
<!DOCTYPE html>
<html lang="br">
<head>
<title>AWS VMs</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="static/css/bootstrap.min.css">
<script src="static/js/jquery.min.js"></script>
<script src="static/js/bootstrap.min.js"></script>
<script src="static/js/custom.js"></script>
</head>
<body>

<div class="container">
<h2>AWS VMs</h2>
<input type="text" id="searchTerm" class="form-control" onkeyup="doSearch()" placeholder="Procurar..">
<p>

<table class="table" id="dataTable">
<tr>
<th onclick="sortTable(0)" style="cursor:pointer">Name</th>
<th onclick="sortTable(1)" style="cursor:pointer">Security Group</th>
<th onclick="sortTable(2)" style="cursor:pointer">Monitoring</th>
<th onclick="sortTable(3)" style="cursor:pointer">IP</th>
<th onclick="sortTable(4)" style="cursor:pointer">State</th>
</tr>
""",
"""
</table>
</div>

</body>
</html>

"""]}
