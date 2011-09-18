<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
    <link href="../../main.css" rel="stylesheet" type="text/css" />
    <title>IRC - entropy.net.nz</title>
  </head>

<body>
  <?php include("navbar.htm"); ?>
    <div id="wrapper">
      <div id="entropymain">
        <h1>New Post</h1>
        <p>
          <form action="new_post.cgi" method="POST">
            Title: <input type="text" name="title"><br />
            Post: <br /><textarea rows="10" cols="100" name="body" />
            <input type="sumbit" value="Post">
          </form>
        </p>
      </div>
    </div>
  </body>
</html>
