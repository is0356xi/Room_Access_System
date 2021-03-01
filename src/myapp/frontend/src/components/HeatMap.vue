<template>
    <div class="Map">
        <div class="parantdiv" id="heatmapContainerWrapper">
            <img class="childimg" src="../../public/static/img/layout.png" />
        </div>
        <div>
            <button v-on:click="Update">ヒートマップ表示</button>
        </div>

        <!-- <div id="heatmapContainerWrapper">
            <div id="heatmapContainer">
            </div>
        </div> -->
        
    </div>
</template>



<script>

// import * as d3 from 'd3';
import * as h337 from 'heatmap.js';

// API用
const axios = require('axios').create()
var heatmap = null
export default {
    
  name: 'HeatMap',
  data() {
      return  {
            heatdata : [

                // // v SCFC
                // { x: 100, y: 182, value: .9 },
                // { x: 120, y: 135, value: .9 },
                // { x: 144, y: 276, value: .9 },
                // { x: 196, y: 272, value: .9 },
                // { x: 121, y: 240, value: .9 },
                // { x: 150, y: 135, value: .9 },
                // { x: 92, y: 135, value: .9 },
                // { x: 96, y: 105, value: .9 },
                // { x: 120, y: 132, value: .9 },
                // { x: 140, y: 157, value: .9 },

                // // v NUFC
                // { x: 80, y: 144, value: .8 },
                // { x: 127, y: 132, value: .8 },
                // { x: 95, y: 148, value: .8 },
                // { x: 94, y: 155, value: .8 },
                // { x: 165, y: 140, value: .8 },
                // { x: 125, y: 147, value: .8 },
                // { x: 110, y: 265, value: .8 },
                // { x: 135, y: 240, value: .8 },
                // { x: 274, y: 376, value: .8 },
                // { x: 245, y: 365, value: .8 },
                // { x: 265, y: 365, value: .8 },
    

                // v AVFC
                // { x: 25, y: 188, value: .8 },
                // { x: 84, y: 290, value: .8 },
                // { x: 92, y: 285, value: .8 },
                // { x: 127, y: 178, value: .8 },
                // { x: 139, y: 127, value: .8 },
                // { x: 165, y: 157, value: .8 },
                // { x: 170, y: 202, value: .8 },
                // { x: 222, y: 255, value: .8 },
                // { x: 348, y: 126, value: .8 },

                // // v THFC
                // { x: 90, y: 222, value: .8 },
                // { x: 97, y: 281, value: .8 },
                // { x: 218, y: 292, value: .8 },
                // { x: 311, y: 238, value: .8 },
                // { x: 225, y: 198, value: .8 },
                // { x: 223, y: 167, value: .8 },
                // { x: 165, y: 164, value: .8 },
                // { x: 371, y: 202, value: .8 },
                // { x: 147, y: 191, value: .8 }

            ]
        }
  },

  

  methods:{
      async Update(){
        console.log("TEST")
        //   this.setData()

        this.setHeatData()

        this.$ready(() => {
            heatmap = h337.create({
                container: document.getElementById('heatmapContainerWrapper'),
                radius: 33,                                               // change radius as required
                blur: .95                                                // blur [0,1]
            });
            window.h = heatmap;
            window.h.setData({
                max: 1,
                data: this.heatdata
            })

            this.heatdata = null
        });
        //   await axios.get('/api/img')
        //   .then(response => {
        //       this.results = response.data;
        //       console.log(this.results);
        //   })
        //   .catch(error => {
        //       console.log(error);
        //   })
      },
      $ready(fn) {
            if (process.env.NODE_ENV === 'production') {
                return this.$nextTick(fn);
            }

            setTimeout(() => {
                this.$nextTick(fn);
                console.log("Next Trick")
            }, 1000);
        },

    //  drawHeat : function() {
    //        // container
    //         var holder = d3.select("#heatmapContainerWrapper")
    //             .append("svg")           // append an SVG element to the div
    //             .attr("width", 550)
    //             .attr("height", 350);

    //         console.log(holder)
    //  }
        async setHeatData(){
            heatmap = null
            const response = await axios.get('/api/test')
            this.heatdata = response.data
            console.log(this.heatdata)
        }
  },
  mounted: function(){
    //   this.drawHeat();
    this.setHeatData()

    // this.$ready(() => {
    //     var heatmap = h337.create({
    //         container: document.getElementById('heatmapContainerWrapper'),
    //         radius: 33,                                               // change radius as required
    //         blur: .95                                                // blur [0,1]
    //     });
    //     window.h = heatmap;
    //     window.h.setData({
    //         max: 1,
    //         data: this.heatdata
    //     })
    //     console.log(this.heatdata)
    // });
  }
}
</script>

<style scoped>
.Map{
  margin-left: auto;
  margin-right: auto;
  text-align: center;
}
.parentdiv{
    display:inline-block;
    background-color:#0000ff;
}
.childimg{
    display:block;
}
</style>