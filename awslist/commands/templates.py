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
<input type="text" id="myInput" class="form-control" onkeyup="search()" placeholder="Procurar..">
<table class="table" id="myTable">

<tr>
<th>Name</th>
<th>Security Group</th>
<th>Monitoring</th>
<th>IP</th>
<th>State</th>
</tr>
""",
"""
</table>
</div>

</body>
</html>

"""]}
