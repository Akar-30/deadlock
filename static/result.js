document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('sequence-container');

    if (resultData.length === 0) {
        const message = document.createElement('p');
        message.className = 'error';
        message.textContent = 'The system is not in a safe state.';
        container.appendChild(message);
    } else {
        resultData.forEach((process, index) => {
            const processDiv = document.createElement('div');
            processDiv.className = 'process';
            processDiv.textContent = `Process ${process + 1}`;
            container.appendChild(processDiv);

            if (index < resultData.length - 1) {
                const arrow = document.createElement('div');
                arrow.className = 'arrow';
                arrow.innerHTML = '&rarr;';
                container.appendChild(arrow);
            }
        });
    }
});