module.exports = {
    content: [
        '../templates/**/*.html',
        './node_modules/flowbite/**/*.js',
        '../node_modules/flowbite/**/*.js',
        '../**/*.js',
    ],
    theme: {
        extend: {
            fontFamily: {
                'factor-a-regular': ['TRIAL Factor A Regular', 'sans'],
                'factor-a-medium': ['TRIAL Factor A Medium', 'sans-serif'],
                'factor-a-bold': ['TRIAL Factor A Bold', 'sans-serif'],
                'inter-semibold': ['Inter SemiBold', 'sans-serif'],
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('flowbite/plugin'),
    ],
}

