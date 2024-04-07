document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var extractedText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.";
    var summarizedText = "Lorem ipsum dolor sit amet.";
    
    document.getElementById('extractedText').textContent = extractedText;
    document.getElementById('summarizedText').textContent = summarizedText;
    document.getElementById('homepage').classList.add('hidden');
    document.getElementById('extractionPage').classList.remove('hidden');
});