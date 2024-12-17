{% include 'navbar.html' %}
        <div class="w-1/2 p-8 bg-white rounded-lg shadow-lg mx-auto">

            {% if 'user_email' in session %}
                <!-- Display Quiz Form if the user is logged in -->
                <h2 class="text-2xl font-semibold text-center mb-6">Welcome, {{ session['user_name'] }}</h2>
                <p class="text-center text-lg text-gray-700 mb-6">Email: {{ session['user_email'] }}</p>
                {% include 'form.html' %}
            {% else %}
                <!-- Show Login Prompt and Form if the user is not logged in -->
                <div class="text-center mb-8">
                    <p class="text-xl font-semibold text-gray-800">Start Your Quiz Journey</p>
                    <p class="mb-4 text-gray-600">Log in to access quizzes and track your progress.</p>
                    <a href="{{ url_for('login') }}" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-full">
                        Login with Google
                    </a>
                </div>

                <!-- Show Quiz Setup Form with Email Input if not logged in -->
                <form action="{{ url_for('quiz') }}" method="post" class="space-y-6">
                    
                    {% include 'form.html' %}
                </form>
            {% endif %}
        </div>