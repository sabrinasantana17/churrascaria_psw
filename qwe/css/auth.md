* { box-sizing: border-box; }
body {
    font-family: Arial, Helvetica, sans-serif;
    margin: 0;
    background: #2b2b2b;
    color: #222;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}
.auth-box {
    width: 100%;
    max-width: 380px;
    background: #fff;
    padding: 28px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
h1 { margin-top: 0; color: #7a1f1f; text-align: center; }
form p { margin: 10px 0; }
input[type=text], input[type=password], input[type=email] {
    width: 100%; padding: 6px 8px; border: 1px solid #ccc; border-radius: 4px;
}
.btn { display: block; width: 100%; background: #7a1f1f; color: #fff; padding: 8px 16px; border-radius: 4px; text-decoration: none; border: none; cursor: pointer; font-size: 14px; }
.btn:hover { background: #5e1717; }
.switch-link { text-align: center; margin-top: 14px; font-size: 14px; }
.messages { list-style: none; padding: 0; }
.messages li { background: #dff0d8; color: #3c763d; padding: 8px 12px; border-radius: 4px; margin-bottom: 10px; }
.errorlist { color: #a94442; list-style: none; padding: 0; margin: 4px 0; }