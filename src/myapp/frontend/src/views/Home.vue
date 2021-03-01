<template>
  <div class="home">
    <h1>研究室 環境モニタリング</h1>
    <div class="box">
        <heat-map />
    </div>
    
    <div class="box">
        <access-table />
    </div>
    
  </div>

  
</template>

<script>
import HeatMap from '../components/HeatMap'
import AccessTable from '../components/AccessTable.vue'
export default {
  components:{
      HeatMap,
      AccessTable
  }
}
</script>

<style scoped>
.box{
    float: left;
    width: auto;
    margin-left: 15px;
}
.home{
    overflow:hidden;
}
</style>
