console.log(student_pk)
console.log(class_room_pk)
var return_data
$.ajax({
    type: "POST",
    url: "/dashboard_api/get_student_log_data",
    data: {
        'student_pk':student_pk,
        'class_room_pk':class_room_pk,
    },
    dataType: "json",
    async:false,
    success: function (response) {
        return_data = JSON.parse(response['data']);
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
    top: '5%',
    left: 'center'
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
        show: false
      },
      data: return_data
    }
  ]
};

option && myChart.setOption(option);
window.addEventListener('resize', function() {
    myChart.resize();
});