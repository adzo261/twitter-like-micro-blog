
document.getElementById("id_content").onkeyup = function () {
      document.getElementById("char_count").innerHTML = 250 - this.value.length;
};


