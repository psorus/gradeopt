

def generatetextbox(name,desc,value="",typ="text"):
  return f'''<label for="{name}">{desc}:</label><br>
  <input type="{typ}" id="{name}" name="{name}" value="{value}"><br>'''

def generateform(callfunc,t,submit="Submit"):
  return f'''<form action="/{callfunc}" method="POST">
{"<br>".join([generatetextbox(**ac) for ac in t])}
<br><br>
  <input type="submit" value="{submit}">
</form> '''

def generatelink(link,text):
  return f'''<a href="{link}">{text}</a>'''

