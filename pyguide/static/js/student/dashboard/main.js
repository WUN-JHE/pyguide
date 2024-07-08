var return_data
$.ajax({
    type: "POST",
    url: "/dashboard_api/get_self_log_data",
    data: {},
    dataType: "json",
    async:false,
    success: function (response) {
        console.log(JSON.parse(response['table']));
        let table_data = JSON.parse(response['table']);
        return_data = JSON.parse(response['data']);
        let body = "";
        for (let index = 0; index < Object.keys(table_data).length; index++) {
          console.log(table_data[index])
          body += `<tr><th scope="row">${table_data[index]['times']}</th><td nowrap="nowrap">${table_data[index]['type']}</td><td>${table_data[index]['des']}</td></tr>`;
        }
        $("#tbody").html(body);
    }
});

var chartDom = document.getElementById('main_circle');
var myChart = echarts.init(chartDom);
var option;

option = {
  tooltip: {
    trigger: 'item'
  },
  legend: {
    top: 'center',
    left: '10%',
    orient: 'vertical',
    show: true,
  },
  series: [
    {
      name: '錯誤類型',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 20,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: true,
        length: 20,
        length2: 50,
        smooth: true
      },
      data: return_data
    }
  ]
};

option && myChart.setOption(option);
window.addEventListener('resize', function() {
    myChart.resize();
});