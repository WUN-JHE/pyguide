var return_data
var series_data = [];
$.ajax({
    type: "POST",
    url: "/dashboard_api/get_self_log_data",
    data: {},
    dataType: "json",
    async:false,
    success: function (response) {
        console.log(JSON.parse(response['table']));
        console.log(JSON.parse(response['data']));
        let table_data = JSON.parse(response['table']);
        return_data = JSON.parse(response['data']);
        return_data.forEach(element => {
            console.log(element);
            series_data.push(
                {
                    name: element['name'],
                    type: 'bar',
                    stack: 'total',
                    label: {
                      show: true
                    },
                    emphasis: {
                      focus: 'series'
                    },
                    data: [element['value']],
                    barWidth: 30
                  }
            )
        });
    }
});

var chartDom = document.getElementById('main_circle');
var myChart = echarts.init(chartDom);
var option;

option = {
    tooltip: {
      trigger: 'item',
      axisPointer: {
        // Use axis to trigger tooltip
        type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
      },
      position: 'bottom'
    },
    legend: {
        show:false
    },
    grid: {
      left: '1%',
      right: '1%',
      bottom: '1%',
      top: '1%',
      containLabel: false
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: [""]
    },
    series: series_data
  };

window.addEventListener('resize', function() {
  var parentWidth = document.querySelector('#tool_bar_pa').clientWidth - 2 * parseInt(window.getComputedStyle(document.querySelector('#tool_bar_pa')).paddingLeft);
  document.querySelector('#tool_bar').style.width = parentWidth + 'px';
  myChart.resize();
});
  
// 初始化时设置初始宽度
window.dispatchEvent(new Event('resize'));

option && myChart.setOption(option);

var myElement = document.getElementById('feedback_container');

myElement.addEventListener('mouseover', function(event) {
  // 滑鼠進入物件時執行的程式碼
  //document.querySelector('#main_circle').style.height = 120 + 'px';
  console.log('Mouse entered the element');
  //myChart.resize();
});
myElement.addEventListener('mouseout', function(event) {
  // 滑鼠離開物件時執行的程式碼
  //document.querySelector('#main_circle').style.height = 50 + 'px';
  console.log('Mouse left the element');
  //myChart.resize();
});