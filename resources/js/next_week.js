document.addEventListener('DOMContentLoaded', function() {

    let current_Week_Start = get_Date_Start_Of_Week(); // Ngày bắt đầu của tuần hiện tại
    let displayed_Week = new Date(current_Week_Start); // Ngày bắt đầu của tuần đang được hiển thị
    let offset = 0;
    
    // Cập nhật tuần hiện tại khi tải trang
    update_Week(displayed_Week, 0);

    // Xử lý sự kiện cho nút "Tuần kế tiếp"
    document.getElementById('next_week').addEventListener('click', function() {
        // Tính ngày bắt đầu của tuần kế tiếp
        displayed_Week.setDate(displayed_Week.getDate() + 7);
        offset += 1;
        update_Week(displayed_Week, offset);
    });

    // Xử lý sự kiện cho nút "Tuần hiện tại"
    document.getElementById('current_week').addEventListener('click', function() {
        displayed_Week = new Date(current_Week_Start); // Đặt lại ngày bắt đầu tuần hiển thị về tuần hiện tại
        update_Week(displayed_Week, 0);
    });

    // Xử lý sự kiện cho nút "Tuần trước"
    document.getElementById('last_week').addEventListener('click', function() {
        // Tính ngày bắt đầu của tuần trước đó
        displayed_Week.setDate(displayed_Week.getDate() - 7);
        offset -= 1;
        update_Week(displayed_Week, offset);
    });

    function get_Date_Start_Of_Week() {
        const today = new Date();
        // Lấy ngày thứ Hai của tuần hiện tại
        return new Date(today.setDate(today.getDate() - today.getDay() + 1));
    }

    function update_Week(startOfWeek, weekOffset) {
        const weekDates = getWeekDates(startOfWeek);
        document.getElementById('mon').innerHTML = `Thứ Hai <br> ${weekDates[0]}`;
        document.getElementById('tue').innerHTML = `Thứ Ba <br> ${weekDates[1]}`;
        document.getElementById('wed').innerHTML = `Thứ Tư <br> ${weekDates[2]}`;
        document.getElementById('thu').innerHTML = `Thứ Năm <br> ${weekDates[3]}`;
        document.getElementById('fri').innerHTML = `Thứ Sáu <br> ${weekDates[4]}`;
        document.getElementById('sat').innerHTML = `Thứ Bảy <br> ${weekDates[5]}`;
        document.getElementById('sun').innerHTML = `Chủ Nhật <br> ${weekDates[6]}`;

        fetch(`/next-week?week_offset=${weekOffset}`)
        .then(response => response.text())
        .then(result => {
            const result_arr = JSON.parse(result);
            const data = result_arr.filtered_items;
            const scheduleBody = document.getElementById('schedule_body');
            scheduleBody.innerHTML = '';

            const date_week_start = new Date(result_arr.week_start);
            const date_week_end = new Date(result_arr.week_end);
            var Start_week_display = formatDate(date_week_start);
            var End_week_display = formatDate(date_week_end);
            
            document.getElementById('calender').innerHTML = `Tuần: ${Start_week_display} - ${End_week_display}`;

            const periods = ['Sáng', 'Chiều', 'Tối'];
            periods.forEach((period, index) => {
                let row = document.createElement('tr');
                let headerCell = document.createElement('td');
                headerCell.innerText = period;
                row.appendChild(headerCell);

                for (let day = 1; day <= 7; day++) {
                    let cell = document.createElement('td');
                    data.forEach(item => {
                        const class_name = 
                            item.Type_class === 'LT' ? ' theory' :
                            item.Type_class === 'TH' ? ' practice' :
                            item.Type_class === 'ON' ? ' online' :
                            item.Type_class === 'EX' ? ' exam' : '';

                        const period_number_from = index === 0 ? 1 : index === 1 ? 7 : 13;
                        const period_number_to = index === 0 ? 6 : index === 1 ? 12 : 15;

                        if (period_number_from <= item.Period_from && item.Period_from <= period_number_to && item.Date_week === day) {
                            const div = document.createElement('div');
                            div.className = `box_info${class_name}`;

                            // Tạo nội dung HTML
                            let innerHTML = `
                                <div class="name_object">${item.Subject}</div>
                                <div>${item.ID_class}</div>
                                <div>Tiết: ${item.Period_from} - ${item.Period_to}</div>
                                <div>Phòng: ${item.Room}</div>
                                <div>GV: ${item.Teacher}</div>
                                <div>Cơ sở: ${item.Learning_facility}</div>
                            `;

                            // Điều kiện cho loại lớp 'TH' hoặc 'EX'
                            if (item.Type_class === 'TH' || item.Type_class === 'EX') {
                                innerHTML += `<div>Nhóm: ${item.Team}</div>`;
                            }

                            // Điều kiện cho loại lớp 'ON'
                            if (item.Type_class === 'ON') {
                                innerHTML += `
                                    <div>Code: ${item.Code_online}</div>
                                    <div>Phần mềm: ${item.Learning_software}</div>
                                `;
                            }

                            // Gán nội dung vào div và thêm vào cell
                            div.innerHTML = innerHTML;

                            cell.appendChild(div);
                        }
                    });
                    row.appendChild(cell);
                }
                scheduleBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching data:', error));


    }


    function getWeekDates(startOfWeek) {
        let weekDates = [];
        for (let i = 0; i < 7; i++) {
            const date = new Date(startOfWeek);
            date.setDate(startOfWeek.getDate() + i);
            weekDates.push(formatDate(date)); // Định dạng ngày theo kiểu Việt Nam
        }
        return weekDates;
    }

    function formatDate(date) {
        const day = date.getDate().toString().padStart(2, '0');  // Thêm số 0 nếu cần
        const month = (date.getMonth() + 1).toString().padStart(2, '0');  // Tháng tính từ 0 nên phải cộng thêm 1
        const year = date.getFullYear();
        
        return `${day}/${month}/${year}`;
    }

});

































































