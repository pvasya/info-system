function validatePrice(input) {
    input.value = input.value.replace(/[^\d.]/g, '');
    if ((input.value.match(/\./g) || []).length > 1) {
        input.value = input.value.slice(0, -1);
        return;
    }
    
    const parts = input.value.split('.');
    if (parts[1] && parts[1].length > 2) {
        input.value = parts[0] + '.' + parts[1].slice(0, 2);
    }
    
    if (input.value < 0) {
        input.value = input.value.replace('-', '');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const priceInput = document.querySelector('form[action="/goods/add"] input[name="price"]');
    if (priceInput) {
        priceInput.addEventListener('input', (e) => validatePrice(e.target));
        
        priceInput.form.addEventListener('submit', (e) => {
            const value = parseFloat(priceInput.value);
            if (isNaN(value) || value <= 0) {
                e.preventDefault();
                alert('Please enter a valid positive price with up to 2 decimal places');
                priceInput.focus();
                return false;
            }
            
            priceInput.value = value.toFixed(2);
            return true;
        });
    }
    document.querySelectorAll('.product.admin .btn.edit').forEach(button => {
      button.addEventListener('click', (e) => {
        e.stopPropagation();
        const productId = button.dataset.productId;
        const card = button.closest('.product');
        const form = document.getElementById(`edit-form-${productId}`);
        
        document.querySelectorAll('.edit-form').forEach(f => {
          if (f.id !== `edit-form-${productId}`) {
            f.style.display = 'none';
          }
        });
        
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
      });
    });
    

    document.querySelectorAll('.product.admin .btn.cancel').forEach(button => {
      button.addEventListener('click', (e) => {
        e.stopPropagation();
        const productId = button.dataset.productId;
        const form = document.getElementById(`edit-form-${productId}`);
        form.style.display = 'none';
      });
    });
    
   
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.edit-form') && !e.target.classList.contains('edit')) {
        document.querySelectorAll('.edit-form').forEach(form => {
          form.style.display = 'none';
        });
      }
    });
    
   
    document.querySelectorAll('.edit-form form').forEach(form => {
      form.addEventListener('click', (e) => {
        e.stopPropagation();
      });
    });

    document.querySelectorAll('.product.user').forEach(card => {
      const counterEl = card.querySelector('.counter');
      const minusBtn = card.querySelector('.minus');
      const plusBtn = card.querySelector('.plus');
      const formAdd = card.querySelector('.form-add');
      const formRem = card.querySelector('.form-remove');

      let count = parseInt(counterEl.dataset.count || counterEl.innerText, 10);
      if (isNaN(count)) count = 0;

      function update() {
        counterEl.innerText = count;
        minusBtn.disabled = (count <= 0);
      }

      update();

      minusBtn.addEventListener('click', () => {
        if (count > 0) {
          count--;
          update();
          formRem.submit();
        }
      });

      plusBtn.addEventListener('click', () => {
        count++;
        update();
        formAdd.submit();
      });
    });

    document.querySelectorAll('.stars').forEach(starsContainer => {
      const goodsId = starsContainer.dataset.goodsId;

      starsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('star')) {
          const rating = parseInt(e.target.dataset.rating);

          fetch('/goods/rate', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              goods_id: goodsId,
              stars: rating
            })
          })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            if (data.success) {
              starsContainer.querySelectorAll('.star').forEach((star, index) => {
                star.classList.toggle('filled', index < data.user_rating);
              });
              const ratingText = starsContainer.closest('.rating').querySelector('.rating-text');
              if (ratingText) {
                ratingText.innerText = `${data.average_rating}/5 (${data.rating_count} reviews)`;
              }
            } else {
              console.error('Rating update failed:', data.error);
              alert('Error: ' + (data.error || 'Failed to update rating'));
            }
          })
          .catch(error => {
            console.error('Error:', error);
            alert('Failed to update rating: ' + error.message);
          });
        }
      });

      starsContainer.addEventListener('mouseenter', (e) => {
        if (e.target.classList.contains('star')) {
          const rating = parseInt(e.target.dataset.rating);
          starsContainer.querySelectorAll('.star').forEach((star, index) => {
            star.classList.toggle('hover', index < rating);
          });
        }
      }, true);

      starsContainer.addEventListener('mouseleave', () => {
        starsContainer.querySelectorAll('.star').forEach(star => {
          star.classList.remove('hover');
        });
      });
    });
  });