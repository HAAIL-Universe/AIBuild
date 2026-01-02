function disableSubmit(form) {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
        btn.disabled = true;
        btn.innerText = 'Saving...';
    }
}

async function copyDigest() {
    const form = document.getElementById('exportForm');
    const formData = new FormData(form);
    
    try {
        const response = await fetch('/export', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const text = await response.text();
            try {
                await navigator.clipboard.writeText(text);
                alert('Digest copied to clipboard!');
            } catch (clipboardErr) {
                // Fallback
                showCopyModal(text);
            }
        } else {
            alert('Failed to generate digest. Please check dates.');
        }
    } catch (err) {
        console.error('Failed to copy:', err);
        alert('Failed to generate digest.');
    }
}

function showCopyModal(text) {
    // Create modal elements
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0,0,0,0.5)';
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.zIndex = '1000';
    
    const content = document.createElement('div');
    content.style.backgroundColor = 'white';
    content.style.padding = '2rem';
    content.style.borderRadius = '8px';
    content.style.maxWidth = '80%';
    content.style.maxHeight = '80%';
    content.style.display = 'flex';
    content.style.flexDirection = 'column';
    
    const title = document.createElement('h3');
    title.innerText = 'Copy Digest';
    content.appendChild(title);
    
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.width = '500px';
    textarea.style.height = '300px';
    textarea.style.margin = '1rem 0';
    content.appendChild(textarea);
    
    const btn = document.createElement('button');
    btn.innerText = 'Close';
    btn.className = 'button secondary';
    btn.onclick = () => document.body.removeChild(modal);
    content.appendChild(btn);
    
    modal.appendChild(content);
    document.body.appendChild(modal);
    
    textarea.select();
}
