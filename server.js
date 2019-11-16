// Modified from
// https://gist.github.com/ryanflorence/701407

const http = require("http"),
  url = require("url"),
  path = require("path"),
  fs = require("fs"),
  port = process.argv[2] || 4040

http.createServer(function(request, response) {

  const uri = url.parse(request.url).pathname
  let filename = path.join(process.cwd(), 'frontend', uri)
  
  fs.stat(filename, function(err,stats) {
    if (err) {
      response.writeHead(404, {'Content-Type': 'text/plain'})
      response.write('404 Not Found\n')
      response.end()
      return
    }

    if (stats.isDirectory()) filename += '/index.html'

    fs.readFile(filename, 'binary', function(err, file) {
      if(err) {
        response.writeHead(500, {'Content-Type': 'text/plain'})
        response.write(err + '\n')
        response.end()
        return
      }
      response.writeHead(200)
      response.write(file, 'binary')
      response.end()
    })
  })
}).listen(parseInt(port, 10))

console.log("Static file server running at\n  => http://localhost:" + port + "/\nCTRL + C to shutdown")