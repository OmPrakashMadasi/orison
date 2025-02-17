$(document).ready(function () {
    $('#mainContent').show();
});

function showItems(category) {
    const products = {
        Shirts: [
            { name: "Girls Uniform", description: "Comfortable school shoes.", cost: "$25", image: "https://images-cdn.ubuy.co.in/6579fd300baff139ec546d46-mufeng-kids-girls-school-uniforms.jpg" },
            { name: "Boys&Girls", description: "Perfect for running and sports.", cost: "$40", image: "https://s.alicdn.com/@sc04/kf/H4dfb151531a3438d97e3cb1cd8de01202.jpg_720x720q50.jpg" },
            { name: "Boy Uniform", description: "Perfect for running and sports.", cost: "$40", image: "https://5.imimg.com/data5/SELLER/Default/2022/11/NW/RN/NP/11329887/half-sleeves-school-shirt-500x500.jpg" },
            { name: "Girl&Boy", description: "Perfect for running and sports.", cost: "$40", image: "https://image.made-in-china.com/202f0j00leubfVidCroh/British-Style-Boys-Girls-School-Uniform-Full-Set-Style-Cotton-Choral-Performance-Clothing.webp" },
        ],
        HALFPANTS: [
            { name: "Half Pants", description: "Classic striped school tie.", image: "https://image.made-in-china.com/202f0j00leubfVidCroh/British-Style-Boys-Girls-School-Uniform-Full-Set-Style-Cotton-Choral-Performance-Clothing.webp" },
            { name: "Half Pants", description: "Elegant plain tie for school.", image: "https://images.jdmagicbox.com/quickquotes/images_main/school-uniform-half-pants-363995859-4pzk0.png" },
            { name: "Half Pants", description: "Elegant plain tie for school.", image: "https://in.all.biz/img/in/catalog/124878.jpeg" },
            { name: "Half Pants", description: "Elegant plain tie for school.", image: "https://5.imimg.com/data5/PR/IN/MY-29300425/brown-half-pants-500x500.jpg" },
        ],
        PANTS: [
            { name: "PANTS", description: "High-quality leather belt.", image: "https://www.globaluniforms.co.in/images/products/school-pants.jpg" },
            { name: "PANTS", description: "Durable canvas belt for school.", image: "https://www.globaluniforms.co.in/images/products/school-pants.jpg" },
            { name: "PANTS", description: "Durable canvas belt for school.", image: "https://s.alicdn.com/@sc04/kf/H1e8b0884131d43bfa2b270fa20ce4663E.png_720x720q50.png" },
            { name: "PANTS", description: "Durable canvas belt for school.", image: "https://5.imimg.com/data5/SELLER/Default/2023/6/316317186/FG/ZC/GL/15921043/boys-school-pants-500x500.jpeg" },
        ],
        DIVIDERSSKIRTS: [
            { name: "DIVIDERSSKIRTS", description: "Comfortable and breathable fabric.", image: "https://ankitgoa.com/wp-content/uploads/2019/03/Jain-School-Uniforms-Kendriya-Vidyalaya-SDL366009275-1-34ee0-500x585.jpg.png" },
            { name: "DIVIDERSSKIRTS", description: "Perfect for physical activities.", image: "https://images.jdmagicbox.com/quickquotes/images_main/girls-polyester-and-viscose-shirt-and-divided-skirt-school-uniform-size-s-m-l-xl-2222383551-olbnrgkb.jpg" },
            { name: "DIVIDERSSKIRTS", description: "Perfect for physical activities.", image: "https://5.imimg.com/data5/CY/NL/MY-57994797/divided-skirt-500x500.jpg" },
            { name: "DIVIDERSSKIRTS", description: "Perfect for physical activities.", image: "https://images.meesho.com/images/products/410678593/rttgu_512.webp" },
        ],
        PINOFORS: [
            { name: "PINOFORS", description: "Comfortable and breathable fabric.", image: "https://5.imimg.com/data5/SELLER/Default/2020/9/PR/ND/XT/4751614/school-pino-tunic-500x500.jpg" },
            { name: "PINOFORS", description: "Perfect for physical activities.", image: "https://i.pinimg.com/originals/fa/0e/0d/fa0e0d43a7d39040b622a2e6eff48d4e.jpg" },
            { name: "PINOFORS", description: "Perfect for physical activities.", image: "https://5.imimg.com/data5/SELLER/Default/2024/2/388623331/TI/CY/PC/105147192/school-uniform.jpeg" },
            { name: "PINOFORS", description: "Perfect for physical activities.", image: "https://5.imimg.com/data5/YV/MM/WU/SELLER-30737602/cotton-se-girls-school-skirt-500x500.jpg" }
        ],
        WHITEFROCK: [
            { name: "WHITEFROCK", description: "Comfortable and breathable fabric.", image: "https://static-01.daraz.lk/p/5ced023e3bcf265ef00a67f0413fd472.png" },
            { name: "WHITEFROCK", description: "Perfect for physical activities.", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWV2FFaZ79Ye7DgHSg5-L_LA6hevDR6-Rf1Q&s" },
            { name: "WHITEFROCK", description: "Perfect for physical activities.", image: "https://cibonline.lk/wp-content/uploads/2023/08/02-30-scaled.jpg" },
            { name: "WHITEFROCK", description: "Perfect for physical activities.", image: "https://5.imimg.com/data5/SELLER/Default/2024/8/440585287/HO/BO/BJ/8834646/school-uniform-shirt-500x500.jpg" }
        ]
    };

    const productDisplay = document.getElementById('productsContainer');
    const welcomeText = document.getElementById('welcomeText');
    const image = document.querySelector('#productDisplay img');
    productDisplay.innerHTML = '';

    welcomeText.style.display = 'none';
    image.style.display = 'none';

    if (products[category]) {
        products[category].forEach(item => {
            const card = document.createElement('div');
            card.className = 'col-md-4 mb-4';
            card.innerHTML = `
                    <div class="card product-card">
                        <img src="${item.image}" class="card-img-top" alt="${item.name}" style="height:200px; width: 100%; object-fit:contain;">
                        <div class="card-body">
                            <h5 class="card-title">${item.name}</h5>
                            <p class="card-text">${item.description}</p>
                           <a href="#" class="btn btn-dark custom-btn">Add to Cart</a>
                            <a href="#" class="btn btn-dark custom-btn" onclick="openModal('${item.name}', '${item.description}', '${item.cost}', '${item.image}')">Buy Now</a>
                        </div>
                    </div>
                `;
            productDisplay.appendChild(card);
        });
    } else {
        productDisplay.innerHTML = '<p class="text-center">No items available in this category.</p>';
    }
}

function openModal(name, description, cost, image) {
    // Set product details in the modal
    document.getElementById('modalProductName').textContent = name;
    document.getElementById('modalProductDescription').textContent = description;
    document.getElementById('modalProductPrice').textContent = cost;
    document.getElementById('modalProductImageSource').src = image;

    // Open the modal
    var myModal = new bootstrap.Modal(document.getElementById('buyNowModal'));
    myModal.show();
}