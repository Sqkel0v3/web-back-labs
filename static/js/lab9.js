document.addEventListener('DOMContentLoaded', function() {
    initSnowflakes();
    
    loadGameState();
});

function initSnowflakes() {
    const snowflakes = document.querySelector('.snowflakes');
    for (let i = 0; i < 50; i++) {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        snowflake.innerHTML = '❄';
        snowflake.style.left = `${Math.random() * 100}%`;
        snowflake.style.animationDuration = `${Math.random() * 5 + 5}s`;
        snowflake.style.animationDelay = `${Math.random() * 5}s`;
        snowflakes.appendChild(snowflake);
    }
}

async function loadGameState() {
    try {
        const response = await fetch('/lab9/api/get_state');
        const data = await response.json();
        
        updateCounters(data.opened_count, data.remaining_boxes);
        
        data.opened_boxes.forEach(boxId => {
            const box = document.getElementById(`box-${boxId}`);
            if (box) {
                box.classList.add('opened');
                box.onclick = null; 
            }
        });
        
        if (data.user_opened_boxes && data.user_opened_boxes.length > 0) {
            loadUserGifts(data.user_opened_boxes);
        }
    } catch (error) {
        console.error('Ошибка загрузки состояния:', error);
    }
}

function updateCounters(opened, remaining) {
    document.getElementById('openedCount').textContent = opened;
    document.getElementById('remainingCount').textContent = remaining;
    
    const progress = (opened / 3) * 100;
    document.getElementById('progressFill').style.width = `${progress}%`;
}

async function openBox(boxId) {
    const box = document.getElementById(`box-${boxId}`);
    
    if (box.classList.contains('opened')) {
        return;
    }
    
    try {
        const response = await fetch('/lab9/api/open_box', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ box_id: boxId })
        });
        
        const result = await response.json();
        
        if (result.success) {
            box.classList.add('opened');
            box.onclick = null;
            
            updateCounters(result.opened_count, result.remaining_boxes);
            
            showCongratulations(result.message, result.gift, boxId);
            
            addGiftToCollection(boxId, result.message, result.gift);
        } else {
            showMessage(result.message, 'error');
        }
    } catch (error) {
        console.error('Ошибка открытия коробки:', error);
        showMessage('Произошла ошибка при открытии коробки', 'error');
    }
}

function showCongratulations(message, gift, boxId) {
    const modal = document.getElementById('messageModal');
    const messageElement = document.getElementById('congratMessage');
    const giftImage = document.getElementById('giftImage');
    
    messageElement.textContent = message;
    
    const giftIcons = ['🎁', '🎄', '⭐', '🦌', '🔔', '⛄', '🧦', '🕯️', '🍪', '🥛'];
    const iconIndex = (boxId - 1) % giftIcons.length;
    giftImage.innerHTML = `<span style="font-size: 4rem;">${giftIcons[iconIndex]}</span>`;
    
    modal.style.display = 'flex';
    
    playSound('open');
}

function closeModal() {
    const modal = document.getElementById('messageModal');
    modal.style.display = 'none';
}

function addGiftToCollection(boxId, message, gift) {
    const container = document.getElementById('giftsContainer');
    const emptyMessage = container.querySelector('.empty-message');
    
    if (emptyMessage) {
        emptyMessage.remove();
    }
    
    const giftCard = document.createElement('div');
    giftCard.className = 'gift-card';
    giftCard.innerHTML = `
        <h3><i class="fas fa-gift"></i> Подарок #${boxId}</h3>
        <div class="gift-card-img">
            <span style="font-size: 3rem;">${getGiftIcon(boxId)}</span>
        </div>
        <p><strong>Поздравление:</strong> ${message}</p>
        <p class="small"><i class="fas fa-calendar"></i> Открыто сегодня</p>
    `;
    
    container.appendChild(giftCard);
}

function getGiftIcon(boxId) {
    const icons = ['🎁', '🎄', '⭐', '🦌', '🔔', '⛄', '🧦', '🕯️', '🍪', '🥛'];
    return icons[(boxId - 1) % icons.length];
}

function showMessage(text, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = text;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#ff4757' : '#2ed573'};
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        z-index: 1001;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        animation: slideInRight 0.3s;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function loadUserGifts(openedBoxes) {
    const container = document.getElementById('giftsContainer');
    container.innerHTML = '';
    
    if (openedBoxes.length === 0) {
        container.innerHTML = '<p class="empty-message">Откройте первую коробку, чтобы увидеть подарок!</p>';
    }
}

async function resetGame() {
    if (!confirm('Вы уверены, что хотите сбросить игру? Все ваши открытые подарки будут потеряны.')) {
        return;
    }
    
    try {
        const response = await fetch('/lab9/reset', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
document.querySelectorAll('.gift-box').forEach(box => {
                box.classList.remove('opened');
                box.onclick = function() {
                    openBox(parseInt(this.dataset.id));
                };
            });
            
            updateCounters(0, 10);
            
            const container = document.getElementById('giftsContainer');
            container.innerHTML = '<p class="empty-message">Откройте первую коробку, чтобы увидеть подарок!</p>';
            
            showMessage('Игра сброшена! Вы можете открыть коробки заново.', 'info');
        }
    } catch (error) {
        console.error('Ошибка сброса:', error);
        showMessage('Ошибка при сбросе игры', 'error');
    }
}

window.onclick = function(event) {
    const modal = document.getElementById('messageModal');
    if (event.target === modal) {
        closeModal();
    }
};