// Giả sử bạn có một API trả về danh sách môn học
fetch('/get-data')
    .then(response => response.json())
    .then(result => {
        var data = result.data;
        const subjectSelect = document.getElementById('subject');
        subjectSelect.innerHTML = `<option value="">Chọn môn học</option>`; 
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.Subject;
            option.textContent = item.Subject;
            option.setAttribute('data-id', item.id);
            subjectSelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching subjects:', error));





    document.getElementById('subject').addEventListener('change', function() {
        const selectedOption = this.selectedOptions[0]; // Lấy option đang chọn
        const id_subject = selectedOption.getAttribute('data-id'); // Lấy giá trị data-id từ option        
        document.getElementById('subject_id').value = id_subject; 

        if (id_subject) {
            // Gọi API để lấy chi tiết môn học
            fetch(`/get-data-details?id_subject=${id_subject}`)
                .then(response => response.json())
                .then(result => {                   
                    document.getElementById('Period_from').value = result.data[0].Period_from;
                    document.getElementById('Period_to').value = result.data[0].Period_to;
                    document.getElementById('Date_start').value = result.data[0].Date_start;
                    document.getElementById('Date_end').value = result.data[0].Date_end;
                    document.getElementById('ID_class').value = result.data[0].ID_class;
                    document.getElementById('date_week').value = result.data[0].Date_week;
                    document.getElementById('Learning_facility').value = result.data[0].Learning_facility;
                    document.getElementById('Room').value = result.data[0].Room;
                    document.getElementById('Teacher').value = result.data[0].Teacher;
                    document.querySelector(`input[name="type_class"][value="${result.data[0].Type_class}"]`).checked = true;
                    document.getElementById('Team').value = result.data[0].Team;
                    document.getElementById('Code_online').value = result.data[0].Code_online;
                    document.getElementById('Learning_software').value = result.data[0].Learning_software;
                })
                .catch(error => console.error('Error fetching subject details:', error));
        }
    });
    






    function getSelectedRadioValue() {
        const radios = document.querySelectorAll('input[name="type_class"]');
        for (const radio of radios) {
            if (radio.checked) {
                return radio.value; 
            }
        }
        return null; 
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        const check_value_form = document.getElementById("submit_form_edit_data");
        check_value_form.addEventListener('submit', function(event) {        
            event.preventDefault();
    
            const form = event.target;
            var id_subject = document.getElementById('subject').value;
            var ID_class = document.getElementById('ID_class').value;
            var date_week = document.getElementById('date_week').value;
            var Period_from = document.getElementById('Period_from').value;
            var Period_to = document.getElementById('Period_to').value;
            var Date_start = document.getElementById('Date_start').value;
            var Date_end = document.getElementById('Date_end').value;
            var Learning_facility = document.getElementById('Learning_facility').value;
            var Room = document.getElementById('Room').value;
            var Teacher = document.getElementById('Teacher').value;
            var Team = document.getElementById('Team').value;
            var Code_online = document.getElementById('Code_online').value;
            var Learning_software = document.getElementById('Learning_software').value;
            var admin_code = document.getElementById('admin_code').value;
            const type_class = getSelectedRadioValue();
            var error = document.getElementById('error_notify_new_data');
    
            if (id_subject.trim() == '') {
                error.textContent = 'Vui lòng nhập chọn môn học!';
                return;
            }
            if (ID_class.trim() == '') {
                error.textContent = 'Vui lòng nhập mã học phần!';
                return;
            }
            if (date_week.trim() == '') {
                error.textContent = 'Vui lòng chọn thứ trong tuần!';
                return;
            }
            if (Period_from.trim() == '') {
                error.textContent = 'Vui lòng chọn tiết bắt đầu!';
                return;
            }
            if (Period_to.trim() == '') {
                error.textContent = 'Vui lòng chọn tiết kết thúc!';
                return;
            }
            if (Date_start.trim() == '') {
                error.textContent = 'Vui lòng chọn ngày bắt đầu học!';
                return;
            }
            if (Date_end.trim() == '') {
                error.textContent = 'Vui lòng chọn ngày kết thúc học!';
                return;
            }
            if (Learning_facility.trim() == '') {
                error.textContent = 'Vui lòng chọn cơ sở học tập!';
                return;
            }
            if (Room.trim() == '') {
                error.textContent = 'Vui lòng nhập phòng học!';
                return;
            }
            if (Teacher.trim() == '') {
                error.textContent = 'Vui lòng nhập tên giảng viên!';
                return;
            }
            if (type_class == null) {
                error.textContent = 'Vui lòng chọn hình thức môn học!';
                return;
            }
            if (admin_code.trim() == '') {
                error.textContent = 'Vui lòng nhập mã admin!';
                return;
            }
    
            if (type_class === "TH") {
                if (Team.trim() == '') {
                    error.textContent = 'Vui lòng nhập nhóm thực hành!';
                    return;
                }
    
            } else if (type_class === "EX") {
                if (Team.trim() == '') {
                    error.textContent = 'Vui lòng nhập nhóm thi!';
                    return;
                }
    
            } else if (type_class === "ON") {
                if (Code_online.trim() == '') {
                    error.textContent = 'Vui lòng nhập mã phòng!';
                    return;
                }
                if (Learning_software.trim() == '') {
                    error.textContent = 'Vui lòng nhập tên ứng dụng học online!';
                    return;
                }
            }
    
            const admin_code_Regex = 20153;    
            if (admin_code != admin_code_Regex) {
                error.textContent = 'Sai mã Admin, vui lòng nhập lại!';
                return;
            }
    
            
            
            const formData = new FormData(form);
            // for (const [key, value] of formData.entries()) {
            //     console.log(key, value);  
            // }
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/change-data', true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    if(response.status == "success"){
                        error.textContent = response.message;
                        form.reset();
                    } else {
                        error.textContent = response.message;
                    }
                }
            };
            xhr.send(formData);
        });
    });