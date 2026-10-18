/**
 * CareerBridge - Client Interaction Engine
 * Handles interactive roadmap updates, skill filtering, drag-and-drop resume upload, and Chart animations
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Bootstrap Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(el => new bootstrap.Tooltip(el));

    // 2. Auto-dismiss Alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 6000);
    });

    // 3. Roadmap Milestone Interactive Status Update
    const statusSelects = document.querySelectorAll('.roadmap-status-select');
    statusSelects.forEach(select => {
        select.addEventListener('change', async (e) => {
            const itemId = e.target.getAttribute('data-item-id');
            const newStatus = e.target.value;
            const cardEl = document.getElementById(`milestone-card-${itemId}`);
            const timelineItemEl = document.getElementById(`timeline-item-${itemId}`);

            e.target.disabled = true;

            try {
                const response = await fetch(`/roadmap/item/${itemId}/status`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({ status: newStatus })
                });

                const data = await response.json();

                if (data.success) {
                    const result = data.data;

                    // Update UI Timeline styles
                    if (timelineItemEl) {
                        timelineItemEl.classList.remove('completed', 'in-progress');
                        if (newStatus === 'Completed') {
                            timelineItemEl.classList.add('completed');
                        } else if (newStatus === 'In Progress') {
                            timelineItemEl.classList.add('in-progress');
                        }
                    }

                    // Update Global Progress Bar if present
                    const progressBar = document.getElementById('roadmap-overall-progress-bar');
                    const progressText = document.getElementById('roadmap-progress-pct-text');
                    const completedCountText = document.getElementById('roadmap-completed-count-text');

                    if (progressBar) {
                        progressBar.style.width = `${result.progress_pct}%`;
                    }
                    if (progressText) {
                        progressText.textContent = `${result.progress_pct}%`;
                    }
                    if (completedCountText) {
                        completedCountText.textContent = result.completed_items;
                    }

                    // Update status badge pill
                    const badgePill = document.getElementById(`status-badge-${itemId}`);
                    if (badgePill) {
                        badgePill.className = 'badge';
                        if (newStatus === 'Completed') {
                            badgePill.classList.add('bg-success');
                            badgePill.innerHTML = '<i class="fa-solid fa-circle-check me-1"></i> Completed';
                        } else if (newStatus === 'In Progress') {
                            badgePill.classList.add('bg-primary');
                            badgePill.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> In Progress';
                        } else {
                            badgePill.classList.add('bg-secondary');
                            badgePill.innerHTML = '<i class="fa-regular fa-clock me-1"></i> Not Started';
                        }
                    }

                    // Subtle feedback toast / visual pulse
                    if (cardEl) {
                        cardEl.style.transition = 'background-color 0.4s ease';
                        cardEl.style.backgroundColor = newStatus === 'Completed' ? '#f0fdf4' : '#f8fafc';
                        setTimeout(() => {
                            cardEl.style.backgroundColor = '#ffffff';
                        }, 800);
                    }
                } else {
                    alert(data.message || 'Failed to update milestone status.');
                }
            } catch (err) {
                console.error('Error updating milestone status:', err);
                alert('Connection error while updating status. Please try again.');
            } finally {
                e.target.disabled = false;
            }
        });
    });

    // 4. Skills Client-Side Filtering
    const skillSearchInput = document.getElementById('skillSearchInput');
    const skillCategoryFilters = document.querySelectorAll('.skill-cat-filter-btn');
    const skillCards = document.querySelectorAll('.skill-item-card');

    let currentCategory = 'all';

    function filterSkills() {
        const query = skillSearchInput ? skillSearchInput.value.toLowerCase().trim() : '';

        let visibleCount = 0;
        skillCards.forEach(card => {
            const name = card.getAttribute('data-skill-name').toLowerCase();
            const category = card.getAttribute('data-skill-category');
            const prof = card.getAttribute('data-skill-prof');

            const matchesSearch = !query || name.includes(query) || category.toLowerCase().includes(query);
            const matchesCat = currentCategory === 'all' || category === currentCategory;

            if (matchesSearch && matchesCat) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        const noResultsMsg = document.getElementById('noSkillsMatchMsg');
        if (noResultsMsg) {
            noResultsMsg.style.display = visibleCount === 0 ? 'block' : 'none';
        }
    }

    if (skillSearchInput) {
        skillSearchInput.addEventListener('input', filterSkills);
    }

    if (skillCategoryFilters.length > 0) {
        skillCategoryFilters.forEach(btn => {
            btn.addEventListener('click', (e) => {
                skillCategoryFilters.forEach(b => b.classList.remove('active', 'btn-cb-primary'));
                skillCategoryFilters.forEach(b => b.classList.add('btn-cb-secondary'));

                btn.classList.add('active', 'btn-cb-primary');
                btn.classList.remove('btn-cb-secondary');

                currentCategory = btn.getAttribute('data-category');
                filterSkills();
            });
        });
    }

    // 5. Resume Drag & Drop Upload Enhancements
    const dropzone = document.getElementById('resumeDropzone');
    const fileInput = document.getElementById('resumeFileInput');
    const fileSelectedBox = document.getElementById('selectedFileInfo');
    const fileNameDisplay = document.getElementById('selectedFileName');
    const fileSizeDisplay = document.getElementById('selectedFileSize');

    if (dropzone && fileInput) {
        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropzone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropzone.classList.remove('dragover');
            }, false);
        });

        dropzone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileSelect(files[0]);
            }
        });

        dropzone.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                handleFileSelect(fileInput.files[0]);
            }
        });
    }

    function handleFileSelect(file) {
        const allowedExtensions = ['pdf', 'docx'];
        const ext = file.name.split('.').pop().toLowerCase();

        if (!allowedExtensions.includes(ext)) {
            alert('Please select a valid .pdf or .docx document.');
            fileInput.value = '';
            if (fileSelectedBox) fileSelectedBox.style.display = 'none';
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            alert('File exceeds the 5MB maximum limit. Please upload a smaller resume.');
            fileInput.value = '';
            if (fileSelectedBox) fileSelectedBox.style.display = 'none';
            return;
        }

        if (fileSelectedBox && fileNameDisplay) {
            fileNameDisplay.textContent = file.name;
            const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);
            if (fileSizeDisplay) fileSizeDisplay.textContent = `${sizeInMB} MB`;
            fileSelectedBox.style.display = 'block';
        }
    }

    // 6. Resume Review Screen: Select All / Deselect All Toggle
    const selectAllCheckbox = document.getElementById('selectAllExtractedSkills');
    const skillCheckboxes = document.querySelectorAll('.extracted-skill-checkbox');
    const selectedCountBadge = document.getElementById('selectedSkillsCounter');

    function updateSelectedSkillsCount() {
        if (!selectedCountBadge) return;
        const checkedCount = document.querySelectorAll('.extracted-skill-checkbox:checked').length;
        selectedCountBadge.textContent = `${checkedCount} selected`;
    }

    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', (e) => {
            skillCheckboxes.forEach(cb => {
                cb.checked = e.target.checked;
            });
            updateSelectedSkillsCount();
        });

        skillCheckboxes.forEach(cb => {
            cb.addEventListener('change', () => {
                const allChecked = Array.from(skillCheckboxes).every(c => c.checked);
                selectAllCheckbox.checked = allChecked;
                updateSelectedSkillsCount();
            });
        });

        updateSelectedSkillsCount();
    }
});
