document.addEventListener("DOMContentLoaded", async function () {

    async function getChartData() {

        try {

            const response = await fetch("/chart-data");

            return await response.json();

        } catch (error) {

            console.error("Chart Data Error:", error);

            return null;

        }

    }

    const chartData = await getChartData();

    // ===========================
    // LINE CHART
    // ===========================

    const lineCanvas = document.getElementById("lineChart");

    if (lineCanvas) {

        new Chart(lineCanvas, {

            type: "line",

            data: {

                labels: [

                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul"

                ],

                datasets: [{

                    label: "Customers",

                    data: [

                        120,
                        170,
                        220,
                        260,
                        320,
                        390,
                        470

                    ],

                    borderColor: "#4F46E5",

                    backgroundColor: "rgba(79,70,229,.12)",

                    fill: true,

                    tension: .4

                }]

            }

        });

    }

    // ===========================
    // PIE CHART
    // ===========================

    const pieCanvas = document.getElementById("pieChart");

    if (pieCanvas && chartData) {

        new Chart(pieCanvas, {

            type: "pie",

            data: {

                labels: [

                    "Active",

                    "Churn"

                ],

                datasets: [{

                    data: [

                        chartData.active,

                        chartData.churn

                    ],

                    backgroundColor: [

                        "#22C55E",

                        "#EF4444"

                    ]

                }]

            }

        });

    }

    // ===========================
    // BAR CHART
    // ===========================

    const barCanvas = document.getElementById("barChart");

    if (barCanvas && chartData) {

        new Chart(barCanvas, {

            type: "bar",

            data: {

                labels: Object.keys(chartData.countries),

                datasets: [{

                    label: "Customers",

                    data: Object.values(chartData.countries),

                    backgroundColor: "#4F46E5"

                }]

            },

            options: {

                plugins: {

                    legend: {

                        display: false

                    }

                }

            }

        });

    }

    // ===========================
    // DOUGHNUT
    // ===========================

    const doughnutCanvas = document.getElementById("doughnutChart");

    if (doughnutCanvas && chartData) {

        const total = chartData.active + chartData.churn;

        const activePercent = Math.round((chartData.active / total) * 100);

        const churnPercent = Math.round((chartData.churn / total) * 100);

        new Chart(doughnutCanvas, {

            type: "doughnut",

            data: {

                labels: [

                    "Active",

                    "Churn"

                ],

                datasets: [{

                    data: [

                        activePercent,

                        churnPercent

                    ],

                    backgroundColor: [

                        "#22C55E",

                        "#EF4444"

                    ]

                }]

            }

        });

    }

});