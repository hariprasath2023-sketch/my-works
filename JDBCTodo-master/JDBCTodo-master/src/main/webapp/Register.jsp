<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
  <title>Registration</title>
</head>
<body>
  <form class="vh-100" style="background-color: white;" action="register" method="POST">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-12 col-md-8 col-lg-8 col-xl-9">
          <div class="card shadow-2-strong" style="border-radius: 1rem;">
            <div class="card-body p-5 text-center">
              <h3 class="mb-5">Register</h3>

              <div class="form-outline mb-4">
                <input type="text" id="typeEmailX-2" class="form-control form-control-lg" name="username" placeholder="Email">
              </div>

              <div class="form-outline mb-4">
                <input type="password" id="typePasswordX-2" class="form-control form-control-lg" name="password" placeholder="Password">
              </div>

              <button class="btn btn-sucess btn-lg btn-block" type="submit">Register</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</body>
</html>
