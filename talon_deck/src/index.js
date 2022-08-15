console.log("index255");

fetch("temp/config.json")
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    console.log(JSON.stringify(data));
  })
  .catch(function () {
    console.log("Booo");
  });
