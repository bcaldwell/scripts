let url = 'https://raw.githubusercontent.com/benjamincaldwell/scripts/master/scripts/fantasy_soccer/player_list.json';

function sortTable(table, col, reverse) {
    var tb = table.tBodies[0], // use `<tbody>` to ignore `<thead>` and `<tfoot>` rows
        tr = Array.prototype.slice.call(tb.rows, 0), // put rows into array
        i;
    reverse = -((+reverse) || -1);
    tr = tr.sort(function (a, b) { // sort rows
        return reverse // `-1 *` if want opposite order
            * (a.cells[col].textContent.trim() // using `.textContent.trim()` for test
                .localeCompare(b.cells[col].textContent.trim())
               );
    });
    for(i = 0; i < tr.length; ++i) tb.appendChild(tr[i]); // append each row in order
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

fetch(url)
.then(res => res.json())
.then((players) => {
  console.log('Checkout this JSON! ', players);

  append_index = 12;
  let t = document.getElementsByClassName("general player-list-table stats-player-list-table")[0];
  let header_row = t.getElementsByTagName("tr")[0];

  th = document.createElement('th');
  th.innerHTML = '<a href="playerlist.aspx?srt=80&dpt=2" title="Price">Price</a>';
  header_row.appendChild(th)

  table_rows = t.getElementsByTagName("tr")
  for (var i = 1, row; row = table_rows[i]; i++) {
  	let x = row.insertCell(append_index);
  	let postition = row.cells[0].innerText.trim()
  	let name = row.cells[1].innerText.trim()
  	let team = row.cells[4].innerText.trim()
  	if (name.endsWith(" New")) {
  		name = name.slice(0, -4)
  	}
  	x.innerHTML = players[postition][team][name]
  }

  if (getParameterByName("srt") == 80) {
    sortTable(t, 12, 1)
  }
  
})
.catch(err => console.error(err));