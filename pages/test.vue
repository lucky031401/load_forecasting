<template>
    <div class="home">
        <LineChart :chartData = "chartData" :options="options"/>
        <button @click="update">create new data</button>
    </div>
</template>

<script>
import LineChart from '@/components/LineChart.vue'

export default {
    name:"Home",
    data(){
        return{
            chartData:{
                labels:[
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "June",
                    "July",
                ],
                datasets:[
                    {
                        label:"data 1",
                        data:[2,10,5,9,0,6,20],
                        backgroundColor:this.gradient,
                        borderColor:"#FC2525",
                        pointBackgroundColor:"rgba(171,71,188,1)"
                    }
                ]
            },
            options:{
                responsive:true,
                maintainAspectRatio:false,
                title:{
                    display:true,
                    text:"My data"
                }
            }
        }
    },
    methods:{
        update(){
            setTimeout(() => {
                console.log('update')
                this.chartData.datasets.push(
                    {
                        label:"data 2",
                        data:[52,50,55,59,50,56,50],
                        backgroundColor:"transparent",
                        borderColor:"#05CBE1",
                        pointBackgroundColor:"rgba(171,71,188,1)"
                    }
                )
                this.chartData = {
                    ...this.chartData,
                }
            },2000)
        }
    },
    components:{
        LineChart
    }
}
</script>
