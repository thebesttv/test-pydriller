require 'linguist'

if ARGV.length < 1
    # read from stdin
    code = STDIN.read
    puts code
    blob = Linguist::Blob.new('stdin', code)
    language = blob.language
else
    # read from file
    file_path = ARGV[0]
    file = Linguist::FileBlob.new(file_path)
    language = file.language
end

if language.nil?
    puts "Unknown"
else
    puts language.name
end