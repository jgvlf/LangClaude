from typing import TypedDict

class Startup(TypedDict):
    name: str
    description: str
    

startups: dict[str, Startup] = {
    "Stripe": Startup(
        name="Stripe",
        description=(
            "Stripe is a technology company that builds economic infrastructure "
            "for the internet. Businesses of every size use Stripe's software "
            "and APIs to accept payments, send payouts, and manage their businesses online."
        )
    ),
    "OpenAI": Startup(
        name="OpenAI",
        description=(
            "OpenAI is an AI research and deployment company. Our mission is to ensure that artificial general intelligence benefits all of humanity. We develop and deploy powerful AI technologies while actively cooperating with other research and policy institutions to create a global community working together to address AGI's global challenges."
        )
    ),
    "Supermecados Savegnago": Startup(
        name="Supermecados Savegnago",
        description="Supermecados Savegnago is a Brazilian supermarket chain that operates over 100 stores across the country. Founded in 1952, Savegnago has grown to become one of the largest grocery retailers in Brazil, offering a wide range of products including fresh produce, meat, dairy, and household items. The company focuses on providing quality products at competitive prices while maintaining a strong commitment to customer service and community engagement."
    ),
}