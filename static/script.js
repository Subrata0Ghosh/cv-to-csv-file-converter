// Initialize the file input plugin with drag and drop enabled
$("input[type='file']").fileinput({
    theme: 'fas', // Use Font Awesome icons
    uploadUrl: '#',  // Set the upload URL (not used since uploadAsync is false)
    uploadAsync: false,  // Upload files synchronously
    showUpload: false,  // Hide the upload button
    showRemove: true,  // Show the remove button
    showPreview: true,  // Hide file preview
    showCaption: true,  // Show the file caption
    allowedFileExtensions: ['pdf', 'docx'],  // Allowed file extensions
    maxFileCount: 15,  // Maximum number of files allowed
    validateInitialCount: true,  // Validate the initial file count
    dropZoneEnabled: true,  // Enable drag and drop
});

// Add an event listener to handle the removal action
$('input[type="file"]').on('filecleared', function(event) {
    // Clear the file input when a file is removed
    $(this).fileinput('clear');
});
