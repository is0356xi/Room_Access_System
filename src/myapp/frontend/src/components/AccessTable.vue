<template>
    <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="in_time"
        label="入室時間"
        width="150">
      </el-table-column>
      <el-table-column
        prop="out_time"
        label="退室時間"
        width="150">
      </el-table-column>
      <el-table-column
        prop="name"
        label="ユーザ名"
        width="150">
      </el-table-column>
      <el-table-column
        prop="access"
        label="入退室状況"
        width="160">
      </el-table-column>
    </el-table>
</template>

<script>
const axios = require('axios').create()

export default {
    data() {
    return {
        tableData: []
        }
    },
    methods:{
        updataTableData: async function () {
            const response = await axios.get('/api/access')
            this.tableData = response.data
        }
    },
    mounted () {
        this.updataTableData()
    }
}
</script>