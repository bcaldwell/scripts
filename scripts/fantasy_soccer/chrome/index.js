let url = 'https://raw.githubusercontent.com/benjamincaldwell/scripts/master/scripts/fantasy_soccer/player_list.json';

fetch(url)
.then(res => res.json())
.then((players) => {
  console.log('Checkout this JSON! ', players);

  append_index = 12;
  let table = document.getElementsByClassName("general player-list-table stats-player-list-table")[0];
  let header_row = table.getElementsByTagName("tr")[0];

  th = document.createElement('th');
  th.innerHTML = '<a href="playerlist.aspx?srt=80&dpt=2" title="Price">Price</a>';
  header_row.appendChild(th)

  table_rows = table.getElementsByTagName("tr")
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

  
})
.catch(err => console.error(err));