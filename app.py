<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ Thống Order Quán Trà Sữa</title>
    <style>
        :root {
            --primary: #ff9a9e;
            --secondary: #fecfef;
            --text: #333;
            --bg: #f4f7f6;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--bg);
            color: var(--text);
            display: flex;
            height: 100vh;
        }
        h1, h2 {
            margin-top: 0;
            color: #444;
        }
        /* Layout chính */
        .menu-section {
            flex: 2;
            padding: 20px;
            overflow-y: auto;
            border-right: 2px solid #ddd;
        }
        .order-section {
            flex: 1;
            padding: 20px;
            background-color: #fff;
            display: flex;
            flex-direction: column;
            box-shadow: -2px 0 5px rgba(0,0,0,0.05);
        }
        /* Lưới Menu */
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }
        .menu-item {
            background: #fff;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .menu-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            border: 2px solid var(--primary);
        }
        .menu-item img {
            width: 100px;
            height: 100px;
            object-fit: cover;
            border-radius: 50%;
            margin-bottom: 10px;
        }
        .menu-item h3 {
            font-size: 16px;
            margin: 10px 0;
        }
        .menu-item p {
            color: #d9534f;
            font-weight: bold;
            margin: 0;
        }
        /* Giỏ hàng */
        .cart-list {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        .cart-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px dashed #ccc;
        }
        .cart-item-info {
            flex: 1;
        }
        .cart-item-name {
            font-weight: bold;
        }
        .cart-item-price {
            font-size: 14px;
            color: #777;
        }
        .cart-actions button {
            background: var(--secondary);
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }
        .cart-actions button:hover {
            background: var(--primary);
            color: #fff;
        }
        .total-section {
            padding-top: 20px;
            border-top: 2px solid #333;
        }
        .total-line {
            display: flex;
            justify-content: space-between;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .btn-checkout {
            width: 100%;
            padding: 15px;
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
        }
        .btn-checkout:hover {
            background-color: #e57373;
        }

        /* Hóa đơn (Chỉ hiển thị khi in) */
        #invoice-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .invoice-content {
            background: #fff;
            padding: 30px;
            width: 400px;
            border-radius: 8px;
            text-align: center;
        }
        .invoice-content h2 { margin-top: 0; }
        .invoice-table { width: 100%; margin: 20px 0; border-collapse: collapse; }
        .invoice-table th, .invoice-table td { border-bottom: 1px solid #ddd; padding: 8px; text-align: left; }
        .invoice-table th { background: #f9f9f9; }
        .invoice-actions { display: flex; gap: 10px; margin-top: 20px; }
        .invoice-actions button {
            flex: 1; padding: 10px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;
        }
        .btn-print { background: #4CAF50; color: white; }
        .btn-close { background: #f44336; color: white; }

        @media print {
            body * { visibility: hidden; }
            #invoice-modal, #invoice-modal * { visibility: visible; }
            #invoice-modal { position: absolute; left: 0; top: 0; background: none; }
            .invoice-actions { display: none; }
        }
    </style>
</head>
<body>

    <!-- Khung Menu Món -->
    <div class="menu-section">
        <h1>🍹 Menu Trà Sữa</h1>
        <div class="menu-grid" id="menu-grid">
            <!-- Danh sách món sẽ được render bằng JS -->
        </div>
    </div>

    <!-- Khung Giỏ Hàng / Hóa Đơn -->
    <div class="order-section">
        <h2>🛒 Đơn Hàng</h2>
        <div class="cart-list" id="cart-list">
            <!-- Sản phẩm được chọn sẽ hiện ở đây -->
        </div>
        <div class="total-section">
            <div class="total-line">
                <span>Tổng cộng:</span>
                <span id="total-price">0 đ</span>
            </div>
            <button class="btn-checkout" onclick="showInvoice()">💳 Thanh toán & Xuất hóa đơn</button>
        </div>
    </div>

    <!-- Hóa đơn (Popup) -->
    <div id="invoice-modal">
        <div class="invoice-content" id="invoice-print-area">
            <h2>HÓA ĐƠN TRÀ SỮA</h2>
            <p>Thời gian: <span id="invoice-time"></span></p>
            <table class="invoice-table">
                <thead>
                    <tr>
                        <th>Tên món</th>
                        <th>SL</th>
                        <th>Thành tiền</th>
                    </tr>
                </thead>
                <tbody id="invoice-items">
                </tbody>
            </table>
            <h3 style="text-align: right;">Tổng thanh toán: <span id="invoice-total">0 đ</span></h3>
            <p>Cảm ơn quý khách và hẹn gặp lại!</p>
            
            <div class="invoice-actions">
                <button class="btn-print" onclick="window.print()">🖨️ In Hóa Đơn</button>
                <button class="btn-close" onclick="closeInvoice()">❌ Đóng & Hủy đơn</button>
            </div>
        </div>
    </div>

    <script>
        // Dữ liệu Menu
        const menuItems = [
            { id: 1, name: 'Trà Sữa Trân Châu', price: 35000, img: 'https://cdn-icons-png.flaticon.com/128/3081/3081162.png' },
            { id: 2, name: 'Trà Sữa Thái Xanh', price: 30000, img: 'https://cdn-icons-png.flaticon.com/128/3081/3081162.png' },
            { id: 3, name: 'Trà Đào Cam Sả', price: 40000, img: 'https://cdn-icons-png.flaticon.com/128/3180/3180302.png' },
            { id: 4, name: 'Hồng Trà Kem Cheese', price: 45000, img: 'https://cdn-icons-png.flaticon.com/128/11790/11790695.png' },
            { id: 5, name: 'Sữa Tươi Trân Châu Đường Đen', price: 45000, img: 'https://cdn-icons-png.flaticon.com/128/3081/3081162.png' },
            { id: 6, name: 'Lục Trà Sữa', price: 32000, img: 'https://cdn-icons-png.flaticon.com/128/3180/3180302.png' }
        ];

        let cart = [];

        // Định dạng tiền tệ VNĐ
        const formatMoney = (amount) => {
            return amount.toLocaleString('vi-VN') + ' đ';
        };

        // Render Menu ra màn hình
        function renderMenu() {
            const menuGrid = document.getElementById('menu-grid');
            menuGrid.innerHTML = '';
            menuItems.forEach(item => {
                menuGrid.innerHTML += `
                    <div class="menu-item" onclick="addToCart(${item.id})">
                        <img src="${item.img}" alt="${item.name}">
                        <h3>${item.name}</h3>
                        <p>${formatMoney(item.price)}</p>
                    </div>
                `;
            });
        }

        // Thêm vào giỏ hàng
        function addToCart(id) {
            const product = menuItems.find(item => item.id === id);
            const existingItem = cart.find(item => item.id === id);

            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                cart.push({ ...product, quantity: 1 });
            }
            renderCart();
        }

        // Tăng giảm số lượng
        function updateQuantity(id, change) {
            const item = cart.find(item => item.id === id);
            if (item) {
                item.quantity += change;
                if (item.quantity <= 0) {
                    cart = cart.filter(cartItem => cartItem.id !== id);
                }
            }
            renderCart();
        }

        // Render Giỏ Hàng
        function renderCart() {
            const cartList = document.getElementById('cart-list');
            const totalPriceEl = document.getElementById('total-price');
            cartList.innerHTML = '';
            let total = 0;

            if (cart.length === 0) {
                cartList.innerHTML = '<p style="text-align:center; color:#999; margin-top:50px;">Chưa có món nào được chọn.</p>';
            }

            cart.forEach(item => {
                const itemTotal = item.price * item.quantity;
                total += itemTotal;
                cartList.innerHTML += `
                    <div class="cart-item">
                        <div class="cart-item-info">
                            <div class="cart-item-name">${item.name}</div>
                            <div class="cart-item-price">${formatMoney(item.price)} x ${item.quantity}</div>
                        </div>
                        <div class="cart-actions">
                            <button onclick="updateQuantity(${item.id}, -1)">-</button>
                            <span>${item.quantity}</span>
                            <button onclick="updateQuantity(${item.id}, 1)">+</button>
                        </div>
                    </div>
                `;
            });

            totalPriceEl.innerText = formatMoney(total);
        }

        // Hiển thị Popup Hóa đơn
        function showInvoice() {
            if (cart.length === 0) {
                alert("Vui lòng chọn món trước khi thanh toán!");
                return;
            }

            const invoiceModal = document.getElementById('invoice-modal');
            const invoiceItems = document.getElementById('invoice-items');
            const invoiceTotal = document.getElementById('invoice-total');
            const invoiceTime = document.getElementById('invoice-time');

            invoiceItems.innerHTML = '';
            let total = 0;

            cart.forEach(item => {
                const itemTotal = item.price * item.quantity;
                total += itemTotal;
                invoiceItems.innerHTML += `
                    <tr>
                        <td>${item.name}</td>
                        <td>${item.quantity}</td>
                        <td>${formatMoney(itemTotal)}</td>
                    </tr>
                `;
            });

            invoiceTotal.innerText = formatMoney(total);
            
            // Set thời gian hiện tại
            const now = new Date();
            invoiceTime.innerText = now.toLocaleString('vi-VN');

            invoiceModal.style.display = 'flex';
        }

        // Đóng hóa đơn và làm mới giỏ hàng
        function closeInvoice() {
            document.getElementById('invoice-modal').style.display = 'none';
            cart = []; // Reset giỏ hàng sau khi tính tiền xong
            renderCart();
        }

        // Chạy lần đầu
        renderMenu();
        renderCart();
    </script>
</body>
</html>
