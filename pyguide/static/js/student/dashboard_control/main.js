//透過ajax取資料庫和錯誤解釋檔的資料出來做成表格
var return_data
$.ajax({
    type: "POST",
    url: "/dashboard_api/get_self_log_des_table",
    data: {},
    dataType: "json",
    async:false,
    success: function (response) {
        console.log(JSON.parse(response['table']));
        let table_data = JSON.parse(response['table']);
        let body = "";
        for (let index = 0; index < Object.keys(table_data).length; index++) {
          console.log(table_data[index])
          body += `<tr><th nowrap="nowrap" scope="row">${table_data[index]['type']}</th><td>${table_data[index]['des']}</td></tr>`;
        }
        $("#tbody").html(body);
    }
});
