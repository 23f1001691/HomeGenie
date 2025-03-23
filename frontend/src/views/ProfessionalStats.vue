<template>
    <div>
        <ProfessionalNav />

    <div class="sidebar">
        <h4>Filters</h4>
        <div class="filter-group">
            <label for="startDateFilter">Start Date</label>
            <input type="date" id="startDateFilter" class="form-control">
        </div>
        <div class="filter-group">
            <label for="endDateFilter">End Date</label>
            <input type="date" id="endDateFilter" class="form-control">
        </div>

        <div class="filter-group">
            <label for="customerFilter">Customer Name</label>
            <input type="text" id="customerFilter" class="form-control" placeholder="Enter customer name">
        </div>
    </div>

    <div class="content">
        <h2>Customer Data</h2>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Date</th>
                    <th>Customer Name</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>2025-01-10</td>
                    <td>John Doe</td>
                    <td>$200</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>2025-01-12</td>
                    <td>Jane Smith</td>
                    <td>$450</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>2025-01-14</td>
                    <td>Michael Brown</td>
                    <td>$320</td>
                </tr>
            </tbody>
        </table>
    </div>

    </div>
    
</template>

<style scoped>
.sidebar {
            height: 100vh;
            position: fixed;
            top: 20;
            left: 0;
            width: 250px;
            background-color: #f8f9fa;
            padding-top: 20px;
            padding-left: 20px;
        }
        .content {
            margin-left: 270px;
            padding: 20px;
        }
        .filter-group {
            margin-bottom: 15px;
        }
</style>


<script>
import ProfessionalNav from "@/components/ProfessionalNav.vue";

export default {
    name: "ProfessionalStats",
    components: {
        ProfessionalNav,
    },
    setup() {
        
        return {
           
        };
    },
};
</script>