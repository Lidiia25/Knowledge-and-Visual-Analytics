{
  const input = document.querySelector('#input');
  const button = document.querySelector('#compute');
  const result = document.querySelector('#result');

  button.onclick = () => {
    let reversed = '';
    for (let i = input.value.length - 1; i >= 0; i--) {
      reversed += input.value[i];
    }
    result.innerText = reversed;
  };
}

//-------------------------------

{
  const input = document.querySelector('#input-number');
  const button = document.querySelector('#make-table');
  const result = document.querySelector('#result-table');

  button.onclick = () => {
    const n = +input.value;
    let x = n;
    let table = '<table>';
    for (let i = 0; i < 5; i++) {
      table += '<tr>';
      for (let j = 0; j < 4; j++) {
        table += '<td>' + x + '</td>';
        x += n;
      }
      table += '</tr>';
    }
    table += '</table>';
    result.innerHTML = table;
  };
}

{
  const presidents = document.querySelector('#presidents');
  const csvUrl = "https://raw.githubusercontent.com/Lidiia25/Knowledge-and-Visual-Analytics-DATA-608/master/Module%206%20HTML%20and%20Javascript/presidents.csv";
  d3.csv(csvUrl).then(function(data) {
    let table = '<table>';
    table += '<tr>';
    for (let j = 0; j < data.columns.length; j++) {
      table += '<td>' + data.columns[j] + '</td>';
    }
    table += '</tr>';

    for (let i = 0; i < data.length; i++) {
      table += '<tr>';
      for (let j = 0; j < data.columns.length; j++) {
        table += '<td>' + data[i][data.columns[j]] + '</td>';
      }
      table += '</tr>';
    }
    table += '</table>';
    presidents.innerHTML = table;
  });
}


{
  const input = document.querySelector('#president-input');
  const button = document.querySelector('#get-president');
  const result = document.querySelector('#president-data');
  const csvUrl = "https://raw.githubusercontent.com/Lidiia25/Knowledge-and-Visual-Analytics-DATA-608/master/Module%206%20HTML%20and%20Javascript/presidents.csv";
  let presidentsData;

  d3.csv(csvUrl).then(function(data) {
    presidentsData = data;
  });

  button.onclick = () => {
    const name = input.value;
    let data = null;
    for (let i = 0; i < presidentsData.length; i++) {
      if (presidentsData[i].Name === name) {
        data = presidentsData[i];
        break;
      }
    }
    if (data) {
      result.innerHTML = `Weight: ${data['Weight']}, Height: ${data['Height']}`;
    }
    else {
      result.innerHTML = 'The name is not correct';
    }
  };
}

{
  const input = document.querySelector('#borough-input');
  const button = document.querySelector('#get-counts');
  const result = document.querySelector('#trees-result');
  const url = "/get_count_spc_by_borough/";

  button.onclick = () => {
    const borough = input.value;

    d3.json(url + borough).then(function(data) {
      let table = '<table>';
      table += '<tr>';
      for (let key in data[0]) {
        table += '<td>' + key + '</td>';
      }
      table += '</tr>';

      for (let i = 0; i < data.length; i++) {
        table += '<tr>';
        for (let key in data[i]) {
          table += '<td>' + data[i][key] + '</td>';
        }
        table += '</tr>';
      }
      table += '</table>';
      result.innerHTML = table;
    });

  };
}