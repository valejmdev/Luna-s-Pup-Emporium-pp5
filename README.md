# Luna's Pup Emporium

## Introduction

Welcome to **Luna's Pup Emporium**, your one-stop shop for high-quality dog gadgets and accessories! Our Django-powered e-commerce site offers a curated selection of products to ensure your furry friend's comfort and style. From durable leashes to cozy beds, we have everything you need to pamper your pup.

This project showcases the integration of Django for backend management, user authentication with Django Allauth, and a user-friendly interface designed to enhance your shopping experience.

### View the live website [here](https://luna-s-pup-emporium-pp5-c2576a3849ce.herokuapp.com)

## User Benefits

### Exceptional Product Range
- **Diverse Categories**: Browse through our categories including Harnesses, Collars, Leashes, Beds, and Toys.
- **Product Details**: View detailed product information including title, description, price, stock, and user reviews.

### Seamless Shopping Experience
- **Search and Sort**: Easily find what you're looking for using our search bar and sorting options by name, price, and rating.
- **User Accounts**: Register, log in, and manage your profile, including order history and details.

### Engaging Features
- **Custom Reviews and Ratings**: Rate products and leave reviews to help others make informed decisions.
- **Cart Management**: Add items to your cart, adjust quantities, and proceed to checkout with ease.

### Comprehensive Support
- **Contact Us**: Send questions or concerns directly to our support team via our Contact Us page.
- **FAQ**: Find answers to common questions quickly in our FAQ section.
- **Terms and Conditions & Privacy Policies**: Review our legal and privacy information to ensure a transparent shopping experience.

### Stay Updated
- **Newsletter**: Subscribe to our newsletter to receive updates, reviews, and special offers.

## Technologies Used

### Backend
- **Django**: The primary web framework used for building the backend of the application.
- **Django Allauth**: Provides user authentication and account management functionalities.
- **Cloudinary**: Integration for managing and delivering media assets, such as product images. Cloudinary offers image storage, transformation, and delivery services, ensuring efficient media handling.
- **dj-database-url**: Facilitates database configuration from environment variables, useful for deploying the application to cloud platforms.
- **django-cloudinary-storage**: Integrates Cloudinary with Django's storage system to handle media files.

### Frontend
- **Bootstrap**: Used for responsive and mobile-first design.
- **Custom CSS and JavaScript**: For additional styling and interactive features.
- **crispy-bootstrap5**: Provides Bootstrap 5 integration with Django forms for enhanced form styling.

### Database
- **SQLite**: Lightweight and easy-to-set-up database used for development.
- **psycopg2**: PostgreSQL adapter for Python, used for connecting to PostgreSQL databases in production.

### Other Libraries
- **Whitenoise**: Used for serving static files efficiently.
- **gunicorn**: WSGI HTTP server for running Django applications in production.
- **stripe**: Integration for handling payment processing.
- **Pillow**: Imaging library for image processing tasks.
- **cryptography**: Provides cryptographic recipes and primitives for secure data handling.
- **PyJWT**: Library for working with JSON Web Tokens, often used for authentication.
- **python-decouple**: Helps manage configuration and environment variables.
- **sqlparse**: A non-GUI SQL parser for handling SQL queries.

## Features

### Product Categories
- **Harnesses**: Adventure Dog Harness, Comfort Fit Harness, Training Harness with Reflective Trim.
- **Collars**: Classic Leather Leash, Colorful Nylon Collar, Custom Engraved Metal Collar, Luxury Leather Collar.
- **Leashes**: Eco-Friendly Rope Leash, Reflective Safety Leash.
- **Beds**: Cozy Canine Haven Bed, Modern Minimalist Bed, Outdoor Adventure Bed.
- **Toys**: Durable Chew Toy, Plush Squeaky Toy, Soft Play Frisbee.

### Shopping Experience
- **Product Sorting**: Sort products by name, price, and rating in both ascending and descending order.
- **Search Functionality**: Find specific products easily using the search bar.

### User Accounts
- **Profile Management**: Users can view, update, and delete their profile information, as well as view their order history.
-  **Order Details**: View detailed information about individual orders.

### Cart and Checkout
- **Cart Details**: View and edit items in the cart, adjust quantities, and proceed to checkout.
- **Checkout**: Provide shipping and payment information for completing purchases.
- **Order Confirmation**: Receive an overview of your order including the order number and total price upon successful payment.


### Content Pages
- **About Us**: Learn about the shop’s mission, the owner, and their passion for dog gadgets.
- **Contact Us**: Send questions, concerns, and issues directly to the shop’s official email.
- **FAQ**: Access answers to frequently asked questions.
- **Terms and Conditions**: Review the terms and conditions governing the use of the site.
- **Privacy Policies**: Understand how user data is collected, used, and protected.

### Newsletter
- **Subscription**: Subscribe to the newsletter to receive updates, benefits, and exclusive content.
## Testing

### Code Validation
- **HTML, CSS, JavaScript, Python**: Validated using respective recommended validators.

### Manual Testing
- **Mobile Testing**: Tested across various devices and screen sizes using Google Chrome Developer Tools and other browsers.

Certainly! Here’s the updated section including details about the newsletter and contact us information:

## Data Storage

Luna's Pup Emporium utilizes PostgreSQL for robust data storage and management, with Cloudinary handling media assets. Here’s how data is organized and managed within the app:

### User Information

- The `User` model in the `users` app stores details such as usernames, email addresses, and password hashes. This information is crucial for user authentication and creating personalized experiences within the shop.

### Products and Categories

- The `Product` and `Category` models in the `products` app manage the storage of product details and categories respectively. This includes product names, descriptions, prices, stock levels, and category associations.

### Orders and Cart Information

- Order details and cart information are tracked through models such as `Order`, `OrderItem`, and `Cart`. These models store information about user orders, items in the cart, quantities, and order statuses, enabling efficient management of purchases and inventory.

### Media Storage

- Cloudinary is used for managing and serving media assets, such as product images and additional visuals. This allows for efficient handling and delivery of high-quality images, ensuring a better user experience on the site.

### Newsletter Subscriptions

- The `NewsletterSubscription` model manages user subscriptions to the newsletter. It stores subscriber email addresses and preferences, allowing for targeted communication and updates about new products, promotions, and other shop news.

### Contact Us Inquiries

- User inquiries submitted through the Contact Us page are stored in the `ContactInquiry` model. This includes user names, email addresses, and message content, which are used to respond to questions, concerns, and issues submitted by users.

## Data Handling and Privacy

### Django ORM Integration

- The app integrates with PostgreSQL using Django’s Object-Relational Mapping (ORM) system. This facilitates smooth database operations and helps maintain a clean and manageable codebase.

### Data Privacy

- Sensitive data, such as user passwords, are hashed before storage using Django’s built-in hashing mechanisms. This ensures that even if the database is compromised, user passwords remain secure.

### Real-Time Updates

- The app updates cart information and order statuses in real-time. This ensures users receive immediate feedback on their purchases and cart modifications.

### Security Measures

- Django’s built-in security features, including SQL injection prevention, cross-site scripting (XSS) protection, and cross-site request forgery (CSRF) protection, are employed to enhance the security of data interactions within the app.

### Static and Media Files Management

- Cloudinary handles the storage and serving of media files, such as product images, ensuring high performance and reliability. Static files, including CSS, JavaScript, and other assets necessary for the front-end, are managed securely to provide optimal performance.

## Deployment

Luna's Pup Emporium was developed using Gitpod and Visual Studio Code for code creation and file management. The project files, code, and related information are hosted on GitHub.

### Deploying the App

To deploy Luna's Pup Emporium on Heroku, follow these steps:

1. **Heroku Account Setup:** Log in to Heroku or create an account if you haven't already.
2. **Create a New App:** From the Heroku dashboard, click on the "New" button and select "Create new app" from the dropdown menu.
3. **App Configuration:** Provide a unique name for your application and select the appropriate region.
   - Example: Name: "lunas-pup-emporium", Region: Europe.
4. **Add Config Vars (if necessary):**
   - If your project requires environment variables, add them under the "Settings" tab in the "Config Vars" section.
5. **Set Buildpacks:**
   - Navigate to the "Settings" tab and locate the "Buildpacks" section.
   - Click on "Add buildpack" and select Python.
   - Ensure the Python buildpack is positioned as the primary buildpack.
6. **Deploy from GitHub:**
   - Go to the "Deploy" section and choose "GitHub" as the deployment method.
   - Connect your GitHub repository to Heroku by searching for the repository name and clicking "Connect".
   - Scroll down and click "Deploy Branch" to deploy the app.
7. **Automatic Deploys (Optional):**
   - If desired, enable automatic deploys to rebuild the app whenever changes are pushed to GitHub.

### Forking The Repository

You can fork the Luna's Pup Emporium repository to create a copy for viewing and editing without affecting the original. Follow these steps:

1. Navigate to the repository on GitHub.
2. Click on the "fork" tab in the top right corner.
3. Click on "create fork" to fork the repository.

### Cloning The Repository

To clone the Luna's Pup Emporium repository from GitHub:

1. Go to the repository and select the "code" tab.
2. Copy the repository's HTTPS URL.
3. Open Git Bash and navigate to the desired directory.
4. Type `git clone` followed by the copied URL and press "enter".

## Credits

### Content
- **Code Institute**: For the structure and guidelines for this project.
- **W3Schools**: For detailed tutorials and references on HTML, CSS, and JavaScript. <https://www.w3schools.com>
- **MDN Web Docs**: For comprehensive documentation on web technologies, including JavaScript and CSS. <https://developer.mozilla.org>
- **Stack Overflow**: For community-driven support and solutions to coding problems encountered during development. <https://stackoverflow.com>
- **Chat GPT**: For helping troubleshoot with code and create content for the website and the README.md. <https://chatgpt.com>
- **Django Documentation**: For resources and guides.
- **Bootstrap Documentation**: For resources and guides.

### Media
- **Font Awesome, Google Fonts**: For enhancing the visual appeal.
- **Microsof Bing Copilot**: For creating all images on the website. <https://www.bing.com/images/create?FORM=GDPGLP>

## Acknowledgements: 
- A very special thanks to Pascal the most helpful person i ever met.  He has helped me tremendously with ideas, fixes and feedback.

- I also want to thank my Mentor Rory-Patrick who gave me so many tips and tricks, and inspired me along the way.

- Also very special thanks to my dog who provided emotional support and times to unwind.
